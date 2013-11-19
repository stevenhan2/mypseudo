## Description:

**mypseudo** is a deployable utility for creating event-based HTTP callbacks (webhooks). It comes with a web interface and a scripting environment for extending functionality. It tries to intelligently emulate the publish-subscribe pattern by timing polls to indicated resources.

## Installation:

*tl;dr* set up MySQL, set up daemon, run webserver

#### Dependencies (Python)
* requests
* beautifulsoup4
* Flask
* MySQLdb

Install:
  
    git clone git://github.com/wufufufu/mypseudo.git

Hopefully running `sudo ./install.sh` or if needed `sudo chmod 755 ./install.sh` first should create the MySQL tables/procedures along with the daemon.

## Usage:

#### Daemon
Run `sudo /etc/init.d/mypseudo start` or `sudo service mypseudo start` to start the polling daemon.

#### Web interface
If you're planning on just using the web interface occasionally and having it off the majority of the time, you can just run the development server with `python server.py`. For a more permanent interface, it's better to pair the WSGI instance with something like Apache. Default port is `:5000`.

## Writing parser scripts:

A callback is paired with a *parser script* that takes the soup from a request and some variables to produce structured content and a decision of whether to actually send a request to the callback url.

See scripts/examplescript.py

## Todo:

* Input sanitization and sanity checks
* Daemon error logging
* Daemon auto restarting
* Write basic RegEx/RSS scripts

