from download_image import download_image

if __name__ == '__main__':
    image_url = 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg'

    img_bytes = download_image(image_url)

    print(img_bytes)