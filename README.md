# Virtual Environment

Commands (from this directory):
* (One time) Create virtual environment: `python3 -m venv .`
* (Every time) Activate virtual environment: `source bin/activate`
* Confirm virtual environment active: `which python` --> `../NoPhoneAI/bin/python`
* Exit virtual environment: `deactivate`

# Dependency Management

1. Install all dependencies: `pip install -r requirements.txt`
2. Add new dependencies: `pip freeze > requirements.txt`

# Useful examples

* https://github.com/twilio/media-streams/blob/master/python/realtime-transcriptions