# Co-working Sign Server

Modular sign writer. 

Add your new module classes to messages/__init__.py

Uses the [alphasign library](https://alphasign.readthedocs.io/en/latest/#) for
communicating with the Aspect 64 LED sign.

# Install

## Auto start at boot

add this to crontab:

	@reboot sleep 60; cd coworking-sign; python sign_writer.py > log 2>&1

sleep is to allow network to get started

## Dependencies

Install python-lxml with apt to avoid very long compiliation times:

	sudo apt-get install python-lxml

Install python dependencies in requirements.txt

	sudo pip install -r requirements.txt

Which will install my alphasign fork from github as pull request to fix sign setup isn't merged.

Twitter display requires secrets, copy the template and then edit it: 

    cp messages/not_twitter_secrets.py messages/twitter_secrets.py

## Watchdog

	sudo apt-get install watchdog

Add this line to the config /etc/watchdog.conf (for whatever your router ip is)

	ping                    = 192.168.1.1
