# Co-working Sign Server

Modular sign writer. 

Add your new module classes to messages/__init__.py

Uses the [alphasign library](https://alphasign.readthedocs.io/en/latest/#) for
communicating with the Aspect 64 LED sign.

# Install

## Auto start at boot

add this to crontab:

	@reboot cd coworking-sign; python sign_writer.py > log 2>&1

## Dependencies

Install python-lxml with apt to avoid very long compiliation times:

	sudo apt-get install python-lxml

Install alphasign from my repo https://github.com/mattvenn/alphasign

Install other dependencies in requirements.txt

	sudo pip install -r requirements.txt

## Watchdog

	sudo apt-get install watchdog

Add this line to the config /etc/watchdog.conf (for whatever your router ip is)

	ping                    = 192.168.1.1
