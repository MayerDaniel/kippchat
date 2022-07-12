import imessage
import re
import os
import random
import urllib
import urllib.request
from bs4 import BeautifulSoup
import pickle
from pprint import pprint
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Conversation, ConversationalPipeline

tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")
nlp = ConversationalPipeline(model=model, tokenizer=tokenizer)
conversation = Conversation()


MESSAGE_CONTENT = 0
GUID = 1

weaponized = False

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Edgar():
    def __init__(self):
        mem_path = 'obj/memories.pkl'
        if not os.path.exists(mem_path):
            os.makedirs(os.path.dirname(mem_path), exist_ok=True)
            self.memories = {}
            save_obj(self.memories,'memories')
        else:
            self.memories = load_obj('memories')
        song_path = 'obj/songs.pkl'

        #send_message(self,string,chatid,noRobot=False)
    def send_message(self, string, guid):
        string = string.replace("'", "")
        string = string.replace('"', '')
        body = """
osascript -e 'tell application "Messages"
  set myid to "%s"
  set mymessage to "%s"
  set theBuddy to a reference to text chat id myid
  send mymessage to theBuddy
end tell' """ % (guid, string)
        print(body)
        resp = os.system(body)
        print("RESPONSE:" + str(resp))
        if resp != 0:
            num = guid.split(";")[-1]
            body = """
osascript -e 'tell application "Messages"
  set targetService to 1st service whose service type = iMessage
  set targetBuddy to buddy "%s" of targetService
  send "%s" to targetBuddy
end tell' """ % (num, string)
            print(body)
            resp = os.system(body)
            print(resp)

    def read(self, message):
        global weaponized
        if not message[MESSAGE_CONTENT]:
            pass
        text = message[MESSAGE_CONTENT].text
        date = message[MESSAGE_CONTENT].date
        command = text.decode().split(" ")
        guid = message[GUID]
        print (command)
        if(command[-1] != ":)"):
            print (guid)
            command = " ".join(command)
            conversation.add_user_input(command)
            result = nlp([conversation], do_sample=False, max_length=500)
            self.send_message(conversation.generated_responses[-1]+" :)", guid)
