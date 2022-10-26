from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters import Text
from aiogram.types import FSInputFile

router = Router()

room_number = 0

@router.message(Text(text='Адрес'))
async def addres_menu(message : Message):
    #Check Address
    if room_number == 0:
        m = ''
        photo = FSInputFile('./source/img/No_address.png')
    else:
        m = 'Твоя комната - ' + room_number
        photo = FSInputFile('./source/img/Address.png')

    #InlineKeyboard setup
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Изменить', callback_data='change')
    )

    #answer
    await message.answer_photo(photo=photo,
        caption= m, 
        reply_markup=builder.as_markup(resize_keyboard=True))