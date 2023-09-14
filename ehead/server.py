#!/usr/bin/env python3
# Email Header Dissector (EHeaD), written in Python and based on Flask aiming at parsing email headers
# and clearly displaying the information in a human readable format
# author: Carmelo C
# email: carmelo.califano@gmail.com
# history, date format ISO 8601:
#  2023-09-13  Forked from https://github.com/cyberdefenders/email-header-analyzer

# Importing modules from Python's standard library
import argparse
from email.parser import HeaderParser   # email: An email and MIME handling package
import time                             # time: Time access and conversions
from datetime import datetime           # datetime: Basic date and time types
import re                               # re: Regular expression operations

# The following modules are to be explicitly installed,
# see `requirements.txt`
# Import Flask, https://flask.palletsprojects.com/
from flask import Flask
from flask import render_template
from flask import request

import dateutil.parser                  # dateutil: Powerful extensions to datetime

import pygal                            # pygal: Beautiful python charting
from pygal.style import Style

from IPy import IP                      # IPy: class and tools for handling of IPv4 and IPv6 addresses and networks
import geoip2.database                  # geoip2: MaxMind GeoIP2 Python API


app = Flask(__name__)
reader = geoip2.database.Reader(f'{app.static_folder}/data/GeoLite2-Country.mmdb')


@app.context_processor
def utility_processor():
    def getCountryForIP(line):
        ipv4_address = re.compile(r"""
            \b((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.
            (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.
            (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.
            (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d))\b""", re.X)
        ip = ipv4_address.findall(line)
        if ip:
            ip = ip[0]  # take the 1st ip and ignore the rest
            if IP(ip).iptype() == 'PUBLIC':
                r = reader.country(ip).country
                if r.iso_code and r.name:
                    return {
                        'iso_code': r.iso_code.lower(),
                        'country_name': r.name
                    }
    return dict(country=getCountryForIP)


@app.context_processor
def utility_processor():
    def duration(seconds, _maxweeks=99999999999):
        return ', '.join(
            '%d %s' % (num, unit)
            for num, unit in zip([
                (seconds // d) % m
                for d, m in (
                    (604800, _maxweeks),
                    (86400, 7), (3600, 24),
                    (60, 60), (1, 60))
            ], ['wk', 'd', 'hr', 'min', 'sec'])
            if num
        )
    return dict(duration=duration)


def dateParser(line):
    try:
        r = dateutil.parser.parse(line, fuzzy=True)

    # if the fuzzy parser failed to parse the line due to
    # incorrect timezone information issue #5 GitHub
    except ValueError:
        r = re.findall('^(.*?)\s*(?:\(|utc)', line, re.I)
        if r:
            r = dateutil.parser.parse(r[0])
    return r


def getHeaderVal(h, data, rex='\s*(.*?)\n\S+:\s'):
    if r := re.findall(f'{h}:{rex}', data, re.X | re.DOTALL | re.I):
        return r[0].strip()
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return render_template('index.html')
    mail_data = request.form['headers'].strip()
    r = {}
    n = HeaderParser().parsestr(mail_data)
    graph = []
    received = n.get_all('Received')
    if received:
        received = [i for i in received if ('from' in i or 'by' in i)]
    else:
        received = re.findall(
            'Received:\s*(.*?)\n\S+:\s+', mail_data, re.X | re.DOTALL | re.I)
    c = len(received)
    for i in range(len(received)):
        if ';' in received[i]:
            line = received[i].split(';')
        else:
            line = received[i].split('\r\n')
        line = list(map(str.strip, line))
        line = [x.replace('\r\n', ' ') for x in line]
        try:
            if ';' in received[i + 1]:
                next_line = received[i + 1].split(';')
            else:
                next_line = received[i + 1].split('\r\n')
            next_line = list(map(str.strip, next_line))
            next_line = [x.replace('\r\n', '') for x in next_line]
        except IndexError:
            next_line = None

        org_time = dateParser(line[-1])
        next_time = org_time if not next_line else dateParser(next_line[-1])
        if line[0].startswith('from'):
            data = re.findall(
                """
                    from\s+
                    (.*?)\s+
                    by(.*?)
                    (?:
                        (?:with|via)
                        (.*?)
                        (?:\sid\s|$)
                        |\sid\s|$
                    )""", line[0], re.DOTALL | re.X)
        else:
            data = re.findall(
                """
                    ()by
                    (.*?)
                    (?:
                        (?:with|via)
                        (.*?)
                        (?:\sid\s|$)
                        |\sid\s
                    )""", line[0], re.DOTALL | re.X)

        delay = (org_time - next_time).seconds
        delay = max(delay, 0)
        try:
            ftime = org_time.utctimetuple()
            ftime = time.strftime('%m/%d/%Y %I:%M:%S %p', ftime)
            r[c] = {
                'Timestmp': org_time,
                'Time': ftime,
                'Delay': delay,
                'Direction': [x.replace('\n', ' ') for x in list(map(str.strip, data[0]))]
            }
            c -= 1
        except IndexError:
            pass

    for i in list(r.values()):
        if i['Direction'][0]:
            graph.append([f"From: {i['Direction'][0]}", i['Delay']])
        else:
            graph.append([f"By: {i['Direction'][1]}", i['Delay']])

    totalDelay = sum(x['Delay'] for x in list(r.values()))
    fTotalDelay = utility_processor()['duration'](totalDelay)
    delayed = bool(totalDelay)

    custom_style = Style(
        background='transparent',
        plot_background='transparent',
        font_family='googlefont:Open Sans',
        # title_font_size=12,
    )
    line_chart = pygal.HorizontalBar(
        style=custom_style, height=250, legend_at_bottom=True,
        tooltip_border_radius=10)
    line_chart.tooltip_fancy_mode = False
    line_chart.title = f'Total Delay is: {fTotalDelay}'
    line_chart.x_title = 'Delay in seconds.'
    for i in graph:
        line_chart.add(i[0], i[1])
    chart = line_chart.render(is_unicode=True)

    summary = {
        'From': n.get('From') or getHeaderVal('from', mail_data),
        'To': n.get('to') or getHeaderVal('to', mail_data),
        'Cc': n.get('cc') or getHeaderVal('cc', mail_data),
        'Subject': n.get('Subject') or getHeaderVal('Subject', mail_data),
        'MessageID': n.get('Message-ID') or getHeaderVal('Message-ID', mail_data),
        'Date': n.get('Date') or getHeaderVal('Date', mail_data),
    }

    security_headers = ['Received-SPF', 'Authentication-Results',
                        'DKIM-Signature', 'ARC-Authentication-Results']
    return render_template(
        'index.html', data=r, delayed=delayed, summary=summary,
        n=n, chart=chart, security_headers=security_headers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Mail Header Analyser")
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="Enable debug mode")
    parser.add_argument("-b", "--bind", default="127.0.0.1", type=str)
    parser.add_argument("-p", "--port", default="8080", type=int)
    args = parser.parse_args()

    app.debug = args.debug
    app.run(host=args.bind, port=args.port)

