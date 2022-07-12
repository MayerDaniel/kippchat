import imessage
import threading
import sys
import time
import os
import logging
import edgarbot
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    sleep_time = 0.1
    def get_Edgar(self, Edgar):
        self.Edgar = Edgar
    def on_modified(self, event):
        messages = imessage.get_last_message()
        threads = []
        for message in messages:
            t = threading.Thread(target=self.Edgar.read(message))
            threads.append(t)
            t.start()

class Listener:
    def __init__(self):
        self.Ed = edgarbot.Edgar()

    def listen(self):
        print ("Edgar is listening!")
        homedir = os.environ['HOME']
        path = homedir + "/Library/Messages/chat.db"
        try:
            while True:
                time.sleep(1)
                messages = imessage.get_last_message()
                threads = []
                for message in messages:
                    t = threading.Thread(target=self.Ed.read(message))
                    threads.append(t)
                    t.start()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def main():
    l = Listener()
    l.listen()

if __name__ == '__main__':
    main()
