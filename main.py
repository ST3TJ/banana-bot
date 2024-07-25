import requests
import re
from random import choice
from telebot import TeleBot, types

# Настройка бота и хоста
BOT_TOKEN = '7384564003:AAH2iM8jOuPzyCdJEzXYdB_4b6T8q3Kijak'
bot = TeleBot(BOT_TOKEN)
HOST = 'https://http.cat/'

# Установка команд бота
bot.set_my_commands([
    types.BotCommand('/start', 'Старт'),
    types.BotCommand('/random', 'Случайная картинка'),
])

# Список HTTP cat изображений
HTTP_CAT_IMAGES = [
    100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404,
    405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444,
    450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 521, 523, 525, 599
]

# Словарь для хранения информации о пользователях
users = {}
dev_list = ['banan2114', 'clmove']

def get_current_unix_time():
    """Возвращает текущее время в формате Unix."""
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
        response.raise_for_status()
        return response.json()['unixtime']
    except requests.RequestException as e:
        print(f"Error fetching time: {e}")
        return None


def log_message(prefix: str, msg: types.Message, user: dict, message_age: int):
    """Логирование информации о сообщении."""
    print(f'{prefix}\nName: {msg.from_user.username}\nText: {msg.text}\nAge: {message_age}\nChat id: {msg.chat.id}\nIgnoring: {user["ignore"]}\nIs Dev: {msg.from_user.username in dev_list}')


def handle_dev_commands(text, chat_id):
    """Обработка команд разработчика."""
    match = re.match(r'/dev (\d+) (.+) (.+)', text)
    if match:
        target_chat_id = int(match.group(1))
        cmd = match.group(2)
        msg = match.group(3)

        if cmd == 'echo':
            bot.send_message(target_chat_id, msg)
        elif cmd == 'ping':
            bot.send_message(target_chat_id, 'pong')
        elif cmd == 'ignore':
            if str(target_chat_id) in users:
                users[str(target_chat_id)]['ignore'] = True
                bot.send_message(chat_id, 'Пользователь будет игнорироваться')
            else:
                bot.send_message(chat_id, 'Пользователь не найден')
        elif cmd == 'unignore':
            if str(target_chat_id) in users:
                users[str(target_chat_id)]['ignore'] = False
                bot.send_message(chat_id, 'Пользователь не будет игнорироваться')
            else:
                bot.send_message(chat_id, 'Пользователь не найден')
        elif cmd == 'time':
            current_time = get_current_unix_time()
            if current_time:
                bot.send_message(target_chat_id, f'Current Unix time: {current_time}')
        else:
            bot.send_message(chat_id, 'Неизвестная команда /dev')
    else:
        bot.send_message(chat_id, 'Неверный формат команды. Используйте /dev <chat_id> <cmd> <msg?>')


def handle_http_cat(text, chat_id):
    """Обработка запросов HTTP cat."""
    try:
        response = requests.get(f"{HOST}{text}")
        if response.status_code == 200:
            bot.send_photo(chat_id, response.url)
        else:
            bot.send_message(chat_id, 'Такой ошибки не существует')
    except requests.RequestException:
        bot.send_message(chat_id, 'Ошибка сети')


@bot.message_handler(func=lambda message: True)
def handle_message(msg: types.Message):
    """Обработчик сообщений."""
    chat_id = msg.chat.id
    text = msg.text

    # Проверка и создание пользователя
    if str(chat_id) not in users:
        users[str(chat_id)] = {'ignore': False}

    user = users[str(chat_id)]
    username = msg.from_user.username

    # Получение возраста сообщения
    current_time = get_current_unix_time()
    if not current_time:
        return

    message_age = current_time - msg.date

    # Логирование сообщений
    if message_age > 10:
        log_message('Old message', msg, user, message_age)
        return
    
    if text.startswith('/dev'):
        log_message('Dev message', msg, user, message_age)
    elif user['ignore']:
        log_message('Ignored message', msg, user, message_age)
        return
    else:
        log_message('New message', msg, user, message_age)

    # Обработка команд и текстовых сообщений
    if text.startswith('/'):
        if text.startswith('/dev') and username in dev_list:
            handle_dev_commands(text, chat_id)
        elif text == '/random':
            bot.send_photo(chat_id, f'{HOST}{choice(HTTP_CAT_IMAGES)}')
        elif text == '/start':
            bot.send_message(chat_id, 'Введите ошибку чтобы узнать что она значит')
        else:
            bot.send_message(chat_id, 'Такой команды нет')
    else:
        handle_http_cat(text, chat_id)

# Запуск бота
bot.polling(non_stop=True, interval=0)