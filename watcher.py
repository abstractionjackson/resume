import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class HTMLHandler(FileSystemEventHandler):
    def __init__(self):
        super(HTMLHandler, self).__init__()

    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'modified' and event.src_path.endswith('.html'):
            print(f"HTML file {event.src_path} has been modified. Relaunching app.py...")
            subprocess.run(['python', 'app.py'])

class SourceCodeHandler(FileSystemEventHandler):
    # watch for changes to .py files like app, classes, utils...
    pass

if __name__ == "__main__":
    path = "templates"  # Change to the directory you want to monitor
    event_handler = HTMLHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"Watching directory {path} for changes...")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
