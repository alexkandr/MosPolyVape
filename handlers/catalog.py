from os import getenv
from aiogram import Router, html
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters import Text
from aiogram.types import FSInputFile, URLInputFile
import pandas as pd

router = Router()

#data from google sheets
SHEET_ID =  getenv('SHEET_ID') #if getenv('SHEET_ID') is str else open('tokens.txt', 'r').readlines()[1].strip()
SHEET_NAME = 'Main'
data_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
data = pd.read_csv(data_url).reset_index()

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
    showing_data = data[data.avaible > 0]
    match _filter:
        case 'lt1000':
            showing_data = showing_data[showing_data.puffs <= 1000]
        case 'lt2000':
            showing_data = showing_data[showing_data.puffs.isin(range(1000,2000))]
        case 'lt4000':
            showing_data = showing_data[showing_data.puffs.isin(range(2000,4000))]
        case 'gt4000':
            showing_data = showing_data[showing_data.puffs >= 4000]
    
    #Check for empty
    if showing_data.empty:
        await call.message.answer(text='Здесь пока ничего нет')
        await call.answer()
        return

    #Show items
    for index, item in showing_data.iterrows():
        keyboard = InlineKeyboardMarkup()
        keyboard
        await call.message.answer_photo(photo= URLInputFile(item.image), caption=(item.description))

    await call.answer()