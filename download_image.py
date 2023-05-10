import requests
from PIL import Image
from io import BytesIO


def download_image(image_url):
    if not image_url.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
        return None

    # Download the image
    response = requests.get(image_url)
    image_content = response.content

    # Create a PIL.Image object from the image content
    image = Image.open(BytesIO(image_content))

    # Save the image as a PNG in a BytesIO stream
    with BytesIO() as output:
        image.save(output, format='PNG')
        image_data = output.getvalue()

    return image_data
