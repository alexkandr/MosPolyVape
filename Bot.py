import telebot
from telebot import types

bot = telebot.TeleBot('5612788804:AAF5Qf8SC1yLjinjGsnGGaDbhI39drR1Uw4')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    match call.data:
        case 'купить':
            bot.register_callback_query_handler()
        case _:
            bot.send_message(text='что-то пошло не так')

@bot.message_handler(content_types=['text'])
def main_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_buy = types.InlineKeyboardButton(text='Купить', callback_data='buy')
    keyboard.add(key_buy)

    key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    keyboard.add(key_back)

    key_cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    keyboard.add(key_cart)

    key_addres = types.InlineKeyboardButton(text='Ну типа адрес', callback_data='addres')
    keyboard.add(key_cart)

    key_contact = types.InlineKeyboardButton(text='Связь', callback_data='contact')
    keyboard.add(key_contact)
    
    bot.send_message(message.from_user.id, 
        text = 'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ', 
        reply_markup=keyboard)




bot.infinity_polling()


