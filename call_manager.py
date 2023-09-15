import json
from twilio.rest import Client

class CallManager:

    def start_terminal_interface(self):
        print("Starting chat. Type quit to exit.")
        twilio_account_sid = json.load(open("creds.json", "r"))["twilio"]["account_sid"]
        twilio_auth_token = json.load(open("creds.json", "r"))["twilio"]["auth_token"]
        client = Client(twilio_account_sid, twilio_auth_token)
        twilio_phone_number = json.load(open("creds.json", "r"))["twilio"]["phone_number"]
        twilio_msg = open("templates/streams.xml", "r").read()
        while True:
            content = input("Phone #: ")

            if content.lower() == "quit":
                print("Quitting chat")
                break

            call = client.calls.create(
                twiml=twilio_msg,
                to=content,
                from_=twilio_phone_number
            )
    

if __name__ == "__main__":
    call_manager = CallManager()
    call_manager.start_terminal_interface()