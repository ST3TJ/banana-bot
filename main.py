# t.me/banan2114bot

from requests import get
from random import randint
from bs4 import BeautifulSoup
from telebot import TeleBot, types

bot = TeleBot('7384564003:AAH2iM8jOuPzyCdJEzXYdB_4b6T8q3Kijak')

http_cat_images = [ 100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 521, 523, 525, 599 ]

@bot.message_handler()
def get_text_messages(msg: types.Message):
    text = msg.text.lower()

    if text.startswith('/'):
        match text:
            case '/random':
                index = http_cat_images[randint(0, len(http_cat_images) - 1)]
                bot.send_photo(msg.from_user.id, 'https://http.cat/' + str(index))
            case _:
                bot.send_message(msg.from_user.id, 'НЕТУ ТАКОЙ КОМАНДЫ ДЕГЕНЕРАТ')
        return
        
    response = get('https://http.cat/' + msg.text)
    if response.status_code != 200:
        bot.send_message(msg.from_user.id, 'НЕТУ ТАКОГО СОСИТЕ')
        return
    bot.send_photo(msg.from_user.id, 'https://http.cat/' + msg.text)

bot.polling(non_stop=True, interval=0)