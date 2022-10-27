from os import getenv
from aiogram import Router, html
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters import Text
from aiogram.types import FSInputFile, URLInputFile
from db.postgre import postgredb

router = Router()

@router.message(Text(text='Каталог'))
async def catalog_menu(message : Message):
    
    #InlineKeyboard setup
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='До 1000 затяжек', callback_data='catalog_lt1000'),
        InlineKeyboardButton(text='1000 - 2000 затяжек', callback_data='catalog_lt2000'),
        InlineKeyboardButton(text='2000 - 4000 затяжек', callback_data='catalog_lt4000'),
        InlineKeyboardButton(text='4000+ затяжек', callback_data='catalog_gt4000')
    )
    builder.adjust(1)

    #answer
    await message.answer_photo(photo=FSInputFile('./source/img/Catalog.png'),
        reply_markup=builder.as_markup(resize_keyboard=True) )

@router.callback_query(Text(text_startswith='catalog_'))
async def show_catalog(call : CallbackQuery):
    
    #Choose appropriate items
    _filter = call.data.split('_')[1]
    showing_data = postgredb.select_by_puffs(_filter)
    
    #Check for empty
    if showing_data == []:
        await call.message.answer(text='Здесь пока ничего нет')
        await call.answer()
        return

    #Show items
    for item in showing_data:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text='В корзину', callback_data=f'add_to_cart_{item.id}'))
        await call.message.answer_photo(photo= URLInputFile(item.image), caption=(item.message_info()),
        reply_markup= builder.as_markup(resize_keyboard=True))

    await call.answer()