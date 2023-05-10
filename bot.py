import telebot
from download_image import download_image
from encryption import Crypto


class Bot:
    def __init__(self):
        password = self.__prompt_password()
        if not password:
            token = self.__prompt_token()
        else:
            token = Crypto.get_token(password)

        self.__run(token)

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

    @staticmethod
    def __run(token):
        bot = telebot.TeleBot(token)

        @bot.message_handler(func=lambda msg: True)
        def echo_all(url):
            image_bytes = download_image(url.text)

            if image_bytes:
                # Send the image back to the user as a PNG in a BytesIO stream
                bot.send_photo(chat_id=url.chat.id, photo=image_bytes, caption='Here is your image!')
            else:
                bot.reply_to(url, 'This is not an image url try again...')

        bot.infinity_polling()
