import os
from PIL import Image
from PIL.ImageOps import grayscale
from watchdog.events import RegexMatchingEventHandler

class ImagesEventHandler(RegexMatchingEventHandler):
    THUMBNAIL_SIZE = (128, 128)
    IMAGES_REGEX = [r".*[^_thumbnail]\.jpg$"]

    def __init__(self):
        # super().__init__(self.IMAGES_REGEX)
        super().__init__()

    def on_created(self, event):
        filename, ext = os.path.splitext(event.src_path)
        print('created ' + filename +"  " + ext)
        # self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}_thumbnail.jpg"

        image = Image.open(event.src_path)
        image = grayscale(image)
        image.thumbnail(self.THUMBNAIL_SIZE)
        image.save(filename)