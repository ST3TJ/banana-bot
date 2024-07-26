# https://t.me/banan2114bot

import requests
import re
from typing import Dict, Optional
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
    types.BotCommand('/dev', 'Для разработчиков')
])

# Список HTTP cat изображений
HTTP_CAT_IMAGES = [
    100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404,
    405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444,
    450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 521, 523, 525, 599
]

# Словари для хранения информации о пользователях
users = {}
dev_list = ['banan2114', 'clmove', 'sqwatnn']
help_message = (
    'Список команд:\n'
    '/dev <id> echo <msg> - отправить сообщение <msg> в чат <id>\n'
    '/dev <id> ping - отправить "pong" в чат <id>\n'
    '/dev <id> ignore - игнорировать пользователя <id>\n'
    '/dev <id> unignore - перестать игнорировать пользователя <id>\n'
    '/dev <id> time - отправить текущее Unix время в чат <id>'
)

def get_current_unix_time():
    """Возвращает текущее время в формате Unix."""
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
        response.raise_for_status()
        return response.json()['unixtime']
    except requests.RequestException as e:
        print(f"Error fetching time: {e}")
        return None


def log_message(prefix: str, msg: types.Message, user: Dict[str, bool], message_age: int):
    """Логирование информации о сообщении."""
    
    username = msg.from_user.username if msg.from_user.username else "Unknown"
    text = msg.text if msg.text else "No text"
    chat_id = msg.chat.id
    ignoring = user.get("ignore", False)
    is_dev = username in dev_list

    log_output = (
        f'{prefix}\n'
        f'Name: {username}\n'
        f'Text: {text}\n'
        f'Age: {message_age}\n'
        f'Chat id: {chat_id}\n'
        f'Ignoring: {ignoring}\n'
        f'Is Dev: {is_dev}\n'
    )

    print(log_output)


def handle_dev_commands(text: str, uid: int):
    """Обработка команд разработчика."""
    
    def is_user_exists(user_id: int) -> bool:
        return str(user_id) in users

    def echo(target: int, msg: str):
        bot.send_message(target, msg)

    def ping(target: int, msg: Optional[str] = None):
        bot.send_message(target, 'pong')

    def ignore(target: int, msg: Optional[str] = None):
        if is_user_exists(target):
            users[str(target)]['ignore'] = True
            bot.send_message(uid, 'Пользователь будет игнорироваться')
        else:
            bot.send_message(uid, 'Пользователь не найден')

    def unignore(target: int, msg: Optional[str] = None):
        if is_user_exists(target):
            users[str(target)]['ignore'] = False
            bot.send_message(uid, 'Пользователь не будет игнорироваться')
        else:
            bot.send_message(uid, 'Пользователь не найден')

    def time(target: int, msg: Optional[str] = None):
        current_time = get_current_unix_time()
        if current_time:
            bot.send_message(target, f'Current Unix time: {current_time}')
    
    commands = {
        'echo': echo,
        'ping': ping,
        'ignore': ignore,
        'unignore': unignore,
        'time': time
    }

    if text in ['/dev', '/dev help']:
        bot.send_message(uid, help_message)
        return

    match = re.match(r'/dev (\w+) (\w+)(?: (.+))?', text)
    if match:
        target = match.group(1)
        target = uid if target == 'self' else int(target)
        cmd = match.group(2)
        msg = match.group(3)

        if cmd in commands:
            if msg is None:
                commands[cmd](target)
            else:
                commands[cmd](target, msg)
        else:
            bot.send_message(uid, 'Неизвестная команда /dev. Используйте /dev help для списка доступных команд.')
    else:
        bot.send_message(uid, 'Неверный формат команды. Используйте /dev <id> <cmd> <msg?>')


def handle_http_cat(text: str, uid: int):
    """Обработка запросов HTTP cat."""
    try:
        response = requests.get(f"{HOST}{text}")
        if response.status_code == 200:
            bot.send_photo(uid, response.url)
        else:
            bot.send_message(uid, 'Такой ошибки не существует')
    except requests.RequestException:
        bot.send_message(uid, 'Ошибка сети')


def handle_command(text, uid, username):
    """Обработчик команд."""
    if text.startswith('/dev'):
        if username in dev_list:
            handle_dev_commands(text, uid)
        else:
            bot.send_message(uid, 'Вы не являетесь разработчиком')
    elif text == '/random':
        bot.send_photo(uid, f'{HOST}{choice(HTTP_CAT_IMAGES)}')
    elif text == '/start':
        bot.send_message(uid, 'Введите код состояния ответа HTTP, чтобы узнать что он значит')
    else:
        bot.send_message(uid, 'Такой команды нет')


@bot.message_handler(func=lambda message: True)
def handle_message(msg: types.Message):
    """Обработчик сообщений."""
    uid = str(msg.chat.id)
    text = msg.text
    username = msg.from_user.username

    # Проверка и создание пользователя
    user = users.setdefault(uid, {'ignore': False})

    # Получение возраста сообщения
    current_time = get_current_unix_time()
    if not current_time:
        return
    message_age = current_time - msg.date

    # Логирование сообщений
    if message_age > 10:
        log_message('Old message', msg, user, message_age)
        return

    if text.startswith('/dev') and username in dev_list:
        log_message('Dev message', msg, user, message_age)
    elif user['ignore']:
        log_message('Ignored message', msg, user, message_age)
        return
    else:
        log_message('New message', msg, user, message_age)

    # Обработка команд и текстовых сообщений
    if text.startswith('/'):
        handle_command(text, uid, username)
    else:
        handle_http_cat(text, uid)

# Запуск бота
bot.polling(non_stop=True, interval=0)