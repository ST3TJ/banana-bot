from telebot import TeleBot

bot = TeleBot('7384564003:AAH2iM8jOuPzyCdJEzXYdB_4b6T8q3Kijak')

def msg_handler(*args, **kwargs):
    print(*args, **kwargs)

bot.add_message_handler(msg_handler)