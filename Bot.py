import telebot
from telebot import types
import pandas as pd


bot = telebot.TeleBot('5612788804:AAF5Qf8SC1yLjinjGsnGGaDbhI39drR1Uw4')
sheet_id = '17p7K08b8-ZGduTy2fgv8IFP6jgdqmidvRH0E6_JQO-Y'
sheet_name = 'Main'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
data = pd.read_csv(url).reset_index()

cart = dict()
room_number = 0

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call.data)
    match call.data:
        case 'l1000':
            show_cat('l1000', call.message)
        case 'l2000':
            show_cat('l2000', call.message)
        case 'l4000':
            show_cat('l4000', call.message)
        case 'g4000':
            show_cat('g4000', call.message)
        case _:
            print('from default')
            error(call.message)

@bot.message_handler(commands=['start'])
def start(message, res=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_cat = types.KeyboardButton('Каталог')
    keyboard.add(key_cat)

    key_cart = types.KeyboardButton('Корзина')
    keyboard.add(key_cart)

    key_addres = types.KeyboardButton('Адрес')
    keyboard.add(key_addres)

    key_contact = types.KeyboardButton('Связь')
    keyboard.add(key_contact)
    
    bot.send_photo(message.from_user.id, photo=open('./source/img/Welcome_Image.png', 'rb'),
        caption= 'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ', 
        reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def main_menu(message):
    match message.text:
        case 'Каталог':
            catalog_menu(message)
        case 'Связь':
            contact_us_menu(message)
        case 'Корзина':
            cart_menu(message)
        case 'Адрес':
            addres_menu(message)
        case _:
            error(message)

def catalog_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_l1000 = types.InlineKeyboardButton(text='До 1000 затяжек', callback_data='l1000')
    keyboard.add(key_l1000)

    key_l2000 = types.InlineKeyboardButton(text='1000 - 2000 затяжек', callback_data='l2000')
    keyboard.add(key_l2000)

    key_l4000 = types.InlineKeyboardButton(text='2000 - 4000 затяжек', callback_data='l4000')
    keyboard.add(key_l4000)

    key_g4000 = types.InlineKeyboardButton(text='4000+ затяжек', callback_data='g4000')
    keyboard.add(key_g4000)

    bot.send_photo(message.from_user.id, photo=open('./source/img/Catalog.png', 'rb'),
        reply_markup=keyboard )

def cart_menu(message):
    cart_mess = cart_to_string(cart)
    if cart == {}:
        bot.send_photo(message.from_user.id, photo=open('./source/img/Empty_cart.png', 'rb'))
        return 

    keyboard = types.InlineKeyboardMarkup()
    
    key_clear = types.InlineKeyboardButton(text='Очистить Корзину', callback_data='clear')
    keyboard.add(key_clear)

    key_buy = types.InlineKeyboardButton(text='Купить', callback_data='buy')
    keyboard.add(key_buy)

    bot.send_photo(message.from_user.id, photo=open('./source/img/Cart.png', 'rb'),
        caption= cart_mess, reply_markup=keyboard)

def addres_menu(message):
    if room_number == 0:
        m = ''
        photo = open('./source/img/No_address.png', 'rb')
    else:
        m = 'Твоя комната - ' + room_number
        photo = open('./source/img/Address.png', 'rb')
    keyboard = types.InlineKeyboardMarkup()
    key_change_addres = types.InlineKeyboardButton(text='Изменить', callback_data='change')
    keyboard.add(key_change_addres)

    bot.send_photo(message.from_user.id, photo=photo,
        caption= m, reply_markup=keyboard)


def contact_us_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_alexkandr = types.InlineKeyboardButton(text='coder: Alexkandr', url='t.me/alexkandr')
    keyboard.add(key_alexkandr)
    key_moony = types.InlineKeyboardButton(text='designer: Moonylofly ', url='t.me/moonylofly')
    keyboard.add(key_moony)
    
    bot.send_photo(message.from_user.id, photo=open('./source/img/Contacts.png', 'rb'),
        caption= 'Что-то не нравится - отсоси ^_^ \n Нахваливать только сообщениями от 1000 символов',
        reply_markup=keyboard)

def show_cat(which, message):
    def none(message):
        bot.send_message(message.chat.id, text='Здесь пока ничего нет')
    def desc(row):
        return row.e_name + '\n' + row.description + '\nВкус    '+ row.taste +'\nТяжек' + str(row.tyazhek) + '\nЦена    ' + str(row.price) + ' рублей'
    match which:
        case 'l1000':            
            showing_data = data[data.tyazhek <= 1000]
            if showing_data.empty:
                none(message)
                return
            for id, d in showing_data.iterrows():
                bot.send_photo( message.chat.id, 
                photo=d.image,
                caption= desc(d))

        case 'l2000':            
            showing_data = data[data.tyazhek.isin(range(1000,2000))]
            
            if showing_data.empty:
                none(message)
                return

            for id, d in showing_data.iterrows():
                bot.send_photo( message.chat.id, 
                photo=d.image,
                caption= desc(d) )
        case 'l4000':            
            showing_data = data[data.tyazhek.isin(range(2000,4000))]
            
            if showing_data.empty:
                none(message)
                return

            for id, d in showing_data.iterrows():
                bot.send_photo( message.chat.id, 
                photo=d.image,
                caption= desc(d) )

        case 'g4000':            
            showing_data = data[data.tyazhek >= 4000]
            
            if showing_data.empty:
                none(message)
                return

            for id, d in showing_data.iterrows():
                bot.send_photo( message.chat.id, 
                photo=d.image,
                caption= desc(d) )
        case _:
            error(message)

def cart_to_string(cart):
    if cart == {}:
        return 'Ваша корзина пуста'
    res = ''
    for key, value in cart:
        res += key + '      ' + value + ' штук'
    return res

def error(message):
    bot.send_photo(message.chat.id, photo=open('./source/img/Error.png', 'rb'), caption='что-то пошло не так')

bot.infinity_polling()


