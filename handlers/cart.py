from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Text
from db.postgre import postgredb

router = Router()

cart = {}

@router.message(Text(text='Корзина'))
async def cart_menu(message : Message):
    
    #check cart
    cart_mess = cart_to_string(cart)
    if cart == {}:
        await message.answer_photo( photo=postgredb.image_by_name('Empty_cart'))
        return 

    #InlineKeyboard setup
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Очистить Корзину', callback_data='clear'),
        InlineKeyboardButton(text='Купить', callback_data='buy')
    )

    #answer
    await message.answer_photo(photo=postgredb.image_by_name('Cart'),
        caption= cart_mess, 
        reply_markup=builder.as_markup(resize_keyboard=True))

def cart_to_string(cart) -> str:
    if cart == {}:
        return 'Ваша корзина пуста'
    res = ''
    for key, value in cart:
        res += key + '      ' + value + ' штук'
    return res