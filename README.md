# Email Header Dissector (EHeaD)

### What is Email Header Dissector (EHeaD)
Email Header Dissector (EHeaD), written in Python and based on [Flask](http://flask.pocoo.org/) aiming at parsing email headers and clearly displaying the information in a human readable format.
EHeaD identifies:
- hop delays
- the source of the email
- hop country

**NOTE**: the tool's name, EHeaD, it to be pronounced `e-hɛd` (just like `e-head`)

### EHeaD is an alternative to the following:
| Name | Dev | Issues |
| ---- | --- | ------ |
| [MessageHeader](https://toolbox.googleapps.com/apps/messageheader/) | Google | Not showing all the hops |
| [EmailHeaders](https://mxtoolbox.com/Public/Tools/EmailHeaders.aspx) | Mxtoolbox | Not accurate and slow |
| [Message Header Analyzer](https://testconnectivity.microsoft.com/MHA/Pages/mha.aspx) | Microsoft | Broken UI |

**All running locally on your Python-enabled laptop!**


### Installation
Clone the GitHub repo:
```
$ git clone https://github.com/carmelo0x63/email-header-dissector.git EHeaD
```

Create a Python3 virtual environment and activate its dependencies:
```
$ cd EHeaD

$ python3 -m venv .

$ source bin/activate

$ python3 -m pip install -r requirements.txt
```
Run the development server:
```
$ cd ehead

$ python3 server.py -d
```

**NOTE**: to make the server accessible from other hosts the following command can be run:
```
$ python3 server.py -d -b 0.0.0.0 -p 8080
```

The following (or similar) messages shall be shown on the console:
```
 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
```

If that is the case, the application can be reached as follows: [http://localhost:8080](http://localhost:8080).

### Docker

A `Dockerfile` is provided if you wish to build a Docker image.

```
$ docker build -t ehead:latest .
```

You can then run a container with:

```
$ docker run -d -p 8080:8080 ehead:latest
```

### Docker-Compose

A `docker-compose` file is provided if you wish to use docker-compose.

Clone the GitHub repo:
```
$ git clone https://github.com/carmelo0x63/email-header-dissector.git EHeaD

$ cd EHeaD
```

Let docker-compose do the work.
```
$ docker-compose up -d
```

Stop the container.
```
$ docker-compose down
```

HowTo enable debugging. Add in the docker `docker-compose.yaml` file the line
```yaml
command: --debug
```

