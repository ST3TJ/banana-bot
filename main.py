from telebot import TeleBot
bot = TeleBot('7384564003:AAH2iM8jOuPzyCdJEzXYdB_4b6T8q3Kijak')

@bot.message_handler()
def get_text_messages(msg):
    bot.send_message(msg.from_user.id, 'Соси)')

bot.polling(none_stop=True, interval=0)