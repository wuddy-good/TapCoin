import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import urllib.parse

TOKEN = '6026382077:AAF2GqgebCbvy-hucLUs7L9BZOE8OfZHeIY'
bot = telebot.TeleBot(TOKEN)

base_url = 'https://randomgamebot.site'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
    }

    query_string = urllib.parse.urlencode(user_data)
    web_app_url = f"{base_url}/user?{query_string}"

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Receive coins", web_app=WebAppInfo(url=web_app_url))],
    ])




if __name__ == '__main__':
    bot.polling()