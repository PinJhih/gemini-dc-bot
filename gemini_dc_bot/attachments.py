from io import BytesIO

import requests
from PIL import Image


def get_images(attachments):
    images = []
    for attachment in attachments:
        if attachment.content_type.startswith("image"):
            res = requests.get(attachment.url)
            image_data = BytesIO(res.content)
            image = Image.open(image_data)
            images.append(image)
    return images
