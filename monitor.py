# file modification watching & idle check

from calendar_integration import addEvent

import os
import time
import datetime
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MONITORED_DIRECTORY = r'C:\Users\Shireen\OneDrive\Desktop\VSCode Codes' #r stands for raw string
INACTIVITY_LIMIT = 30 * 60    # 30 minutes of no file modification/creation
INVALIDITY_DURATION = 10 * 60  #10 min duration sessions (or less) marked as 'null'

class fileHandler(FileSystemEventHandler):
    def __init__(self):
        self.sessionActive = False  #session start/stop
        self.sessionStart = None    #start time
        self.lastActive = time.time() #last activity time
        self.project = None    #last modified folder ie project worked on during session
        self.inactivity_thread = threading.Thread(target=self.inactivity_monitor)  #idle checking
        self.inactivity_thread.daemon = True # allows the main thread to exit even if this thread is running
        self.inactivity_thread.start()
        
    def on_modified(self, _):
        self.lastActive = time.time()
        
        if not self.sessionActive: #session hasnt started
            self.sessionStart = datetime.datetime.now()
            print(f"Session started at {self.sessionStart}")
            self.sessionActive = True
    
    def get_last_modified_folder(self):
        # 'project folder' will be added as part of the event name
        
        if not os.path.isdir(MONITORED_DIRECTORY):
            print(f"Error: Directory '{MONITORED_DIRECTORY}' does not exist.")
            self.project = "Error"
            return
       #
        subdirectories = [d for d in os.listdir(MONITORED_DIRECTORY) if os.path.isdir(os.path.join(MONITORED_DIRECTORY, d))]
        
        if not subdirectories:
            self.project = "General"
            return   # no subdirectories found

        latest_mod_time = 0
        last_modified_folder = None

        for subdir in subdirectories:
            full_path = os.path.join(MONITORED_DIRECTORY, subdir)
            mod_time = os.path.getmtime(full_path)
            if mod_time > latest_mod_time:
                latest_mod_time = mod_time
                last_modified_folder = subdir
        
        self.project = last_modified_folder

    def inactivity_monitor(self):
        while(True):
            time.sleep(10)  # every 10 seconds
            inactive_time = time.time() - self.lastActive # time since last file modification
            sessionEnd = datetime.datetime.now()
            if self.sessionActive and (inactive_time > INACTIVITY_LIMIT): 
                duration = sessionEnd - self.sessionStart
                if duration.total_seconds() > INVALIDITY_DURATION: # long session
                    self.get_last_modified_folder()
                    print(f"Session ended at {sessionEnd}, Duration: {duration}, Project: Coding Session: {self.project}")
                    addEvent(self.sessionStart,sessionEnd, 'Coding Session: ' + str(self.project))
                self.sessionActive = False
                      
# runs script until keyboard interrupt  
if __name__ == "__main__":
    # initialize logging event handler
    event_handler = fileHandler()

    # initialize observer
    observer = Observer()
    observer.schedule(event_handler, path=MONITORED_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()