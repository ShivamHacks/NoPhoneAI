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
* FFmpeg: https://ffmpeg.org/

# Usage

## Call server

1. Start call server:  `python call_server`
2. Forward the port using ngrok: `ngrok http 8080`
3. Set the stream url to the ngrok url in `templates/streams.xml`
4. Start the call manager terminal interface: `python call_manager`
5. Follow the instructions there to start a call

# APIs

* OpenAI ChatGPT
* Assembly AI for real time speech to text
* Eleven Labs for text-to-speech

To consider
* EdenAI - abstracts away Assembly AI, gCloud, and a few others

# TODO

* Create bi-directional Twilio stream: https://www.twilio.com/docs/voice/twiml/stream#bi-directional-media-streams
* Latency KPIs & metrics logging
* Recording both ends of call & saving transcripts for evaluation
* Handling multiple calls concurrently
* Proper call handling, e.g. interrupt AI talking when human talks

# Similar services

* https://www.callbotapp.com/
* https://voicebot.ai/2017/07/27/john-done-will-execute-tasks-behalf-like-waiting-hold

# Helpful examples

* https://www.assemblyai.com/docs/Guides/real-time_streaming_transcription
* https://github.com/twilio/media-streams/blob/master/python/realtime-transcriptions
* https://github.com/AssemblyAI/youtube-tutorials/blob/main/phone-call-transcribe/index.js
* https://github.com/rahulbanerjee26/twilio_assemblyai/blob/main/call.py
* https://github.com/AssemblyAI/twilio-realtime-tutorial/blob/master/transcribe.js?ref=assemblyai.com
