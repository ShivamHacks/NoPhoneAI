import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class ChatManager:

    def __init__(self):
        self.openai_api_key = json.load(open("creds.json", "r"))["openai_api_key"]
    
    def setup_chat(self, name, business, objective, verbose):
        system_template = """I want you to act as me, {name}, talking on the phone with
        {business}. I am unable talk, so I will be using you ChatGPT as a dialogue
        generator for a phone call, and feeding it to a text to speech system.
        You are calling with the objective: “{objective}”. Be nice, and end call when
        objective is completed. Let me know when call is done with string “END CALL”.
        All of your responses should include call dialogue that I will say verbally,
        and nothing else. I am now live on the phone call.

        Previous conversation:
        {{chat_history}}
        """.format(name=name, business=business, objective=objective)

        human_template = "{text}"

        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        self.chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=self.openai_api_key),
            prompt=chat_prompt,
            memory=ConversationBufferMemory(memory_key="chat_history"),
            verbose=verbose
        )
    
    def run(self, content):
        return self.chain.run(content)
    
    def start_terminal_interface(self):
        name = input("Name (default=John Smith): ") or "John Smith"
        business = input("Business (default=Walgreens): ") or "Walgreens"
        objective = input("Objective (default=Check if they have dayquill in stock): ") or "Check if they have dayquill in stock"
        verbose = input("Verbose (default=True): ") or "True"
        self.setup_chat(name, business, objective, verbose)

        print("Starting chat. Type quit to exit.")
        while True:
            content = input("Walgreens: ")

            if content.lower() == "quit":
                print("Quitting chat")
                break

            response = self.run(content)
            print("Bot: " + response)

            if "END CALL" in response:
                print("Call ended.")
                break

if __name__ == "__main__":
    chat_manager = ChatManager()
    chat_manager.start_terminal_interface()
