import requests
from random import choice
from telebot import TeleBot, types


bot = TeleBot('7384564003:AAH2iM8jOuPzyCdJEzXYdB_4b6T8q3Kijak')
host = 'https://http.cat/'

bot.set_my_commands([
    types.BotCommand('/start', 'Старт'),
    types.BotCommand('/random', 'Случайная картинка'),
])

http_cat_images = [100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 521, 523, 525, 599]

@bot.message_handler(func=lambda message: True)
def handle_message(msg: types.Message):
    text = msg.text.lower()
    chat_id = msg.chat.id

    print(f'Name: {msg.from_user.full_name}\nText: {text}\n')

    def send_photo(image_url):
        bot.send_photo(chat_id, image_url)

    def send_message(text):
        bot.send_message(chat_id, text)

    if text.startswith('/'):
        if text == '/random':
            index = choice(http_cat_images)
            send_photo(f"{host}{index}")
        elif text == '/start':
            send_message('Введите ошибку чтобы узнать что она значит')
        else:
            send_message('Такой команды нет')
    else:
        try:
            response = requests.get(f"{host}{text}")
            if response.status_code == 200:
                send_photo(response.url)
            else:
                send_message('Такой ошибки не существует')
        except requests.RequestException:
            send_message('Ошибка сети')

bot.polling(non_stop=True, interval=0)

print('Bot sucessfully started')