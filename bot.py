import telebot
import requests

from encryption import Crypto
from PIL import Image
from io import BytesIO


class Bot:
    def __init__(self):
        password, bot_name = self.__prompt_password(), None

        if not password:
            token = self.__prompt_token()
        else:
            token, bot_name = Crypto.get_token(password), Crypto.get_bot_name(password)

        self.__run(token, bot_name)

    @staticmethod
    def __run(token, bot_name):
        bot = telebot.TeleBot(token)

        print('Successfully started bot polling!\n'
              'go to telegram and message:')
        if bot_name:
            print(bot_name)
        else:
            print("The bot with the name you've just created")

        print('\nYou can try this image URL:\n'
              'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg')

        @bot.message_handler(func=lambda msg: True)
        def echo_all(url):
            image_bytes = Bot.__download_image(url.text)

            if image_bytes:
                # Send the image back to the user as a PNG in a BytesIO stream
                bot.send_photo(chat_id=url.chat.id, photo=image_bytes, caption='Here is your image!')
            else:
                bot.reply_to(url, 'This is not an image url try again...')

        bot.infinity_polling()

    @staticmethod
    def __download_image(image_url):
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

    @staticmethod
    def __prompt_password():
        pw = input('If you have a password for my bot input password.\n '
                   'If not press enter.\n'
                   'Here: ')
        if pw == '' or len(pw) < 5:
            return None
        else:
            return pw

    @staticmethod
    def __prompt_token():
        return input('Since you dont have a password for my bot go to\n'
                     'Telegram site and make your own,\n'
                     'Paste its token here:')
