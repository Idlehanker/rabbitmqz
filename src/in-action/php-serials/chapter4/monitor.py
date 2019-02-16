#!/usr/bin/env python
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import os

class AutoCompileEventHandler(LoggingEventHandler):

    def monite(self, file):
        self.filename = file
        
    def on_modified(self, event):
        super(AutoCompileEventHandler, self).on_modified(event)

        '''
        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)
        '''
        #execfile('alert_consumer.py')
        if len(self.filename) > 1 :
            os.system('python ' + self.filename)
            #os.system('python alert_consumer.py')

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO,
    logging.basicConfig(level=logging.WARN,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    file = sys.argv[2] if len(sys.argv) > 2 else ''
    
    #event_handler = LoggingEventHandler()
    event_handler = AutoCompileEventHandler()
    event_handler.monite(file)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
