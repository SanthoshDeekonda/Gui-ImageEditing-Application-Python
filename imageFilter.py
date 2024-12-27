from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove

class Filters:
    def __init__(self):
        self.factor = 1.0

        self.filters = {
            "Brightness" : lambda img, factor: ImageEnhance.Brightness(img).enhance(factor),
            "Sharpness" : lambda img, factor: ImageEnhance.Sharpness(img).enhance(factor),
            "Blur": lambda img, factor: img.filter(ImageFilter.GaussianBlur(factor)),
            "Rotate Left": lambda img, factor=None: img.rotate(90, expand=True),
            "Rotate Right": lambda img, factor=None: img.rotate(-90, expand=True),
            "Mirror": lambda img, factor=None: img.transpose(Image.FLIP_LEFT_RIGHT),
            "B/W": lambda img, factor=None: img.convert("L"),
            "Remove Background": lambda img, factor=None: remove(img)
        }
    
    def apply_filter(self,img: Image, filter, factor=None) -> Image:
        img = self.filters[filter](img, factor)
        return img
    
    def compare_img(self, image_obj1: Image, image_obj2: Image) -> bool:
        img_1 = list(image_obj1.getdata())
        img_2 = list(image_obj2.getdata())

        if img_1 == img_2:
            return True
        else:
            return False