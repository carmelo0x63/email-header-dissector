## Email Header Dissector (EHeaD)

## What is Email Header Dissector (EHeaD)
Email Header Dissector (EHeaD) is a tool written in [Flask](http://flask.pocoo.org/) for parsing email headers and converting them to a human readable format and it also can:
* Identify hop delays.
* Identify the source of the email.
* Identify hop country.


## EHeaD is an alternative to the following:
| Name | Dev | Issues |
| ---- | --- | ----- |
| [MessageHeader](https://toolbox.googleapps.com/apps/messageheader/) | Google | Not showing all the hops. |
| [EmailHeaders](https://mxtoolbox.com/Public/Tools/EmailHeaders.aspx) | Mxtoolbox | Not accurate and slow. |
| [Message Header Analyzer](https://testconnectivity.microsoft.com/MHA/Pages/mha.aspx) | Microsoft | Broken UI. |


## Installation
Clone the GitHub repo:
```
$ git clone https://github.com/carmelo0x99/email-header-dissector.git
```

Create a Python3 virtual enironment and activate its dependencies:
```
$ cd email-header-dissector
$ python3 -m venv .
$ source bin/activate
$ pip3 install -r requirements.txt
```
Run the development server:
```
$ cd ehead
$ python3 server.py -d
```

You can change the bind address or port by specifying the appropriate options:
```
$ python3 server.py -b 0.0.0.0 -p 8080
```

Everything should go well, now visit [http://localhost:8080](http://localhost:8080).

## Docker

A `Dockerfile` is provided if you wish to build a docker image.

```
docker build -t ehead:latest .
```

You can then run a container with:

```
docker run -d -p 8080:8080 ehead:latest
```

### Docker-Compose

A `docker-compose` file is provided if you wish to use docker-compose.

Clone the GitHub repo:
```
$ git clone https://github.com/carmelo0x99/email-header-dissector.git
$ cd email-header-analyzer
```

Let docker-compose do the work.
```
$ docker-compose up -d
```

Stop the container.
```
$ docker-compose down
```

HowTo enable debugging. Add in the docker `docker-compose.yml` file the line
```yaml
command: --debug
```

