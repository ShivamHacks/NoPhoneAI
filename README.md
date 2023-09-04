# Virtual Environment

Commands (from this directory):
* (One time) Create virtual environment: `python3 -m venv .`
* (Every time) Activate virtual environment: `source bin/activate`
* Confirm virtual environment active: `which python` --> `../NoPhoneAI/bin/python`
* Exit virtual environment: `deactivate`

# Dependency Management

1. Install all dependencies: `pip install -r requirements.txt`
2. Add new dependencies: `pip freeze > requirements.txt`

Special dependencies
* PyAudio: https://pypi.org/project/PyAudio

# APIs

* OpenAI ChatGPT
* Assembly AI for real time speech to text

# Helpful examples

* https://www.assemblyai.com/docs/Guides/real-time_streaming_transcription
* https://github.com/twilio/media-streams/blob/master/python/realtime-transcriptions