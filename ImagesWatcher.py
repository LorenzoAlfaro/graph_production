import sys
import time
from watchdog.observers import Observer
from functions.ImagesEventHandler import ImagesEventHandler

# https://blog.magrathealabs.com/filesystem-events-monitoring-with-python-9f5329b651c3

class ImagesWatcher:
    def __init__(self, src_path):
        self.__src_path = src_path
        self.__event_handler = ImagesEventHandler()
        self.__event_observer = Observer()

    def run(self):
        print("start observing" + self.__src_path)
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )

if __name__ == "__main__":
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    ImagesWatcher(src_path).run()