import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'C:\\Users\\FinnC.DESKTOP-J259HOQ\\Documents'
    event_handler = PatternMatchingEventHandler(patterns=['*employee_ssn_data.xlsx'])
    event_handler.on_modified = LoggingEventHandler().on_modified
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()