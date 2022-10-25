import telebot
from telebot import types

bot = telebot.TeleBot('5612788804:AAF5Qf8SC1yLjinjGsnGGaDbhI39drR1Uw4')

cart = dict()

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call.data)
    match call.data:
        case 'buy':
            bot.register_next_step_handler(call.message, buy_menu)
        case _:
            print('from default')
            bot.send_message(call.message.chat.id, text='что-то пошло не так')

@bot.message_handler(commands=['start'])
def start(message, res=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_buy = types.KeyboardButton('Купить')
    keyboard.add(key_buy)

    key_cart = types.KeyboardButton('Корзина')
    keyboard.add(key_cart)

    key_addres = types.KeyboardButton('Адрес')
    keyboard.add(key_addres)

    key_contact = types.KeyboardButton('Связь')
    keyboard.add(key_contact)
    
    bot.send_message(message.from_user.id, 
        text = 'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ', 
        reply_markup=keyboard )

@bot.message_handler(content_types=['text'])
def main_menu(message):
    match message.text:
        case 'Купить':
            categories_menu(message)
        case 'Связь':
            contact_us_menu(message)
        case 'Корзина':
            cart_menu(message)
        case 'Адрес':
            addres_menu(message)
        case _:

            bot.send_message(message.from_user.id, text='что-то пошло не так')

def categories_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_l1000 = types.InlineKeyboardButton(text='До 1000 затяжек', callback_data='l1000')
    keyboard.add(key_l1000)

    key_l2000 = types.InlineKeyboardButton(text='1000 - 2000 затяжек', callback_data='l2000')
    keyboard.add(key_l2000)

    key_l4000 = types.InlineKeyboardButton(text='2000 - 4000 затяжек', callback_data='l4000')
    keyboard.add(key_l4000)

    key_g4000 = types.InlineKeyboardButton(text='4000+ затяжек', callback_data='g4000')
    keyboard.add(key_g4000)

    bot.send_message(message.from_user.id, 
        text = 'Выберите категорию', 
        reply_markup=keyboard )

def cart_menu(message):
    cart_mess = cart_to_string(cart)
    if cart == {}:
        bot.send_message(message.from_user.id, text = cart_mess)
        return 

    keyboard = types.InlineKeyboardMarkup()
    
    key_clear = types.InlineKeyboardButton(text='Очистить Корзину', callback_data='clear')
    keyboard.add(key_clear)

    key_buy = types.InlineKeyboardButton(text='Купить', callback_data='buy')
    keyboard.add(key_buy)

    bot.send_message(message.from_user.id, 
        text = cart_mess, reply_markup=keyboard)

#def addres_menu(message):


def contact_us_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_alexkandr = types.InlineKeyboardButton(text='coder: Alexkandr', url='t.me/alexkandr')
    keyboard.add(key_alexkandr)
    key_moony = types.InlineKeyboardButton(text='designer: Moonylofly ', url='t.me/moonylofly')
    keyboard.add(key_moony)

    bot.send_message(message.from_user.id, 
        text = 'Что-то не нравится - отсоси ^_^ \n Нахваливать только сообщениями от 1000 символов',
        reply_markup=keyboard)

def cart_to_string(cart):
    if cart == {}:
        return 'Ваша корзина пуста'
    res = ''
    for key, value in cart:
        res += key + '      ' + cart[i] + ' штук'
    return res


bot.infinity_polling()


