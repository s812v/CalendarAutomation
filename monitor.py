# file modification watching & idle check

import time
import datetime
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from py_idle_time import get_idle_duration

MONITORED_DIRECTORY = r'C:\Users\Shireen\OneDrive\Desktop\VSCode Codes' #r stands for raw string
INACTIVITY_LIMIT = 30 * 60    # 30 minutes of no file modification/creation
INVALIDITY_DURATION = 10 * 60  #10 min duration sessions (or less) marked as 'null'


class fileHandler(FileSystemEventHandler):
    def __init__(self):
        self.sessionActive = False  #session start/stop
        self.sessionStart = None    #start time
        self.lastActive = time.time() #last activity time
        self.inactivity_thread = threading.Thread(target=self.inactivity_monitor)  #idle checking
        self.daemon = True # allows the main thread to exit even if this thread is running
        self.inactivity_thread.start()

    def on_modified(self,event):
        #print(f'File {event.src_path} was modified')
        self.lastActive = time.time()
        
        if not self.sessionActive: #session hasnt started
            self.sessionStart = datetime.datetime.now()
            print(f"Session started at {self.sessionStart}")
            self.sessionActive = True
    
    def inactivity_monitor(self):
        while(True):
            time.sleep(10)  # every 10 seconds
            idle_time = get_idle_duration() # mouse/keyboard movement
            inactive_time = time.time() - self.lastActive # last file modification within directory
            if self.sessionActive and (inactive_time > INACTIVITY_LIMIT or idle_time > INACTIVITY_LIMIT):
                sessionEnd = datetime.datetime.now()
                duration = sessionEnd - self.sessionActive
                print(f"Session ended at {sessionEnd}, Duration: {duration}")
                #addEvent here
                self.sessionActive = False


    #if duration of session lesser than INACTIVITY_DURATION, invalid 

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