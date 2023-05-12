import telebot
import requests

from encryption import Crypto
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse


class Bot:
    def __init__(self):
        token, bot_name = self.__prompt_password()
        self.__run(token, bot_name)

    @staticmethod
    def __run(token, bot_name):
        bot = telebot.TeleBot(token)

        print('Token is valid! Go to telegram and message:')
        if bot_name:
            print(bot_name)
        else:
            print("The bot with the name you've just created")

        print('\nYou can try this image URL:\n'
              'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg')

        @bot.message_handler(func=lambda msg: True)
        def echo_all(reply):
            text = reply.text
            validation: bool | str = Bot.__is_valid_url(text)
            if isinstance(validation, bool):
                # Download image turn to PNG in BytesIO stream & send it back to the user
                image_bytes = Bot.__download_image(text)
                bot.send_photo(chat_id=reply.chat.id, photo=image_bytes, caption='Here is your image!')
            else:
                bot.reply_to(reply, validation)

        bot.infinity_polling()

    @staticmethod
    def __is_valid_url(url: str) -> bool | str:
        try:
            result = urlparse(url)
            is_url: bool = all([result.scheme, result.netloc])
            if is_url:
                if url.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
                    return True
                else:
                    return 'This url does not lead to an image, try sending a url which does point to one!'
            else:
                return 'This is not a url, send a url to an image if you want it back!'
        except:
            return 'This is not a url, send a url to an image if you want it back!'

    @staticmethod
    def __download_image(image_url):
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
    def __prompt_token() -> str | None:
        token = input('Since you dont have a password for my bot go to\n'
                      'Telegram site and make your own,\n'
                      'Paste its token here:')
        if Bot.__is_valid_bot_token(token):
            return token
        else:
            return None

    @staticmethod
    def __is_valid_bot_token(token):
        try:
            bot = telebot.TeleBot(token)
            bot.get_me()
            return True
        except:
            return False

    @staticmethod
    def __prompt_password():
        password = input('If you have a password for my bot input password.\nIf not press enter.\nHere: ')
        if password == '' or len(password) < 5:
            while True:
                token = Bot.__prompt_token()
                if Bot.__is_valid_bot_token(token):
                    return token, None
                else:
                    print('\nInvalid Token\n')
        else:
            token = Crypto.get_token(password)
            bot_name = Crypto.get_bot_name(password)
            if not (token and bot_name):
                print('\nInvalid password\n')
                return Bot.__prompt_password()
            else:
                return token, bot_name

