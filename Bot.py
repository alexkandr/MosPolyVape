import telebot
from telebot import types

bot = telebot.TeleBot('5612788804:AAF5Qf8SC1yLjinjGsnGGaDbhI39drR1Uw4')

@bot.message_handler(content_types=['text'])
def main_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_buy = types.InlineKeyboardButton(text='Купить', callback_data='buy')
    keyboard.add(key_buy)

    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard.add(key_back)
    
    bot.send_message(message.from_user.id, 
        text = 'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ', 
        reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)


