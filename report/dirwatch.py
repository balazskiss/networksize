from watchdog.observers import Observer
from watchdog.events import *
import ntpath


class ReportEventHandler(FileSystemEventHandler):

    def __init__(self, path, callback):
        self.callback = callback
        self.extensions = [".csv"]
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def on_any_event(self, event):
        if not event.is_directory:
            filename, file_extension = os.path.splitext(event.src_path)
            basename = ntpath.basename(event.src_path)
            if file_extension in self.extensions:
                self.callback(event.event_type, basename)

