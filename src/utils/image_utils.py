import cv2
import numpy as np
from PIL import Image
import io

class ImageUtils:
    @staticmethod
    def resize_image(image, width=None, height=None):
        if width and height:
            return cv2.resize(image, (width, height))
        elif width:
            ratio = width / image.shape[1]
            dim = (width, int(image.shape[0] * ratio))
            return cv2.resize(image, dim)
        elif height:
            ratio = height / image.shape[0]
            dim = (int(image.shape[1] * ratio), height)
            return cv2.resize(image, dim)
        return image

    @staticmethod
    def convert_cv2_to_pil(cv2_image):
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv2_image)
        return pil_image

    @staticmethod
    def convert_pil_to_cv2(pil_image):
        numpy_image = np.array(pil_image)
        cv2_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        return cv2_image

    @staticmethod
    def image_to_bytes(image):
        is_success, buffer = cv2.imencode(".jpg", image)
        if is_success:
            return buffer.tobytes()
        return None

    @staticmethod
    def bytes_to_image(image_bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
