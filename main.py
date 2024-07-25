import requests
from random import choice
from telebot import TeleBot, types


bot = TeleBot('7384564003:AAH2iM8jOuPzyCdJEzXYdB_4b6T8q3Kijak')
host = 'https://http.cat/'

bot.set_my_commands([
    types.BotCommand('/start', 'СТАРТУЕМ'),
    types.BotCommand('/random', 'ПОЛУЧАЕМ СМЕШНУЮ КАРТИНКУ С КАТОМ ( +AURA +ВАЙБ +ДЕНЬГИ +КОТ +ФУМО )'),
])

http_cat_images = [100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 521, 523, 525, 599]

@bot.message_handler(func=lambda message: True)
def handle_message(msg: types.Message):
    text = msg.text.lower()

    def send_photo(image_url):
        bot.send_photo(msg.from_user.id, image_url)

    def send_message(text):
        bot.send_message(msg.from_user.id, text)

    if text.startswith('/'):
        if text == '/random':
            index = choice(http_cat_images)
            send_photo(f"{host}{index}")
        elif text == '/start':
            send_message('КУДА СТАРТУЕМ ТО')
        else:
            send_message('НЕТУ ТАКОЙ КОМАНДЫ ДЕГЕНЕРАТ')
    else:
        try:
            response = requests.get(f"{host}{text}")
            if response.status_code == 200:
                send_photo(response.url)
            else:
                send_message('НЕТУ ТАКОГО СОСИТЕ')
        except requests.RequestException:
            send_message('ОШИБКА В СЕТИ')

bot.polling(non_stop=True, interval=0)