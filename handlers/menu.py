from aiogram import Router
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.dispatcher.filters import Text
from aiogram.types import FSInputFile

router = Router()
@router.message(commands=["start"])
async def start(message : Message):
    #ReplyKeyboard setup
    builder = ReplyKeyboardBuilder()
    for name in ['Каталог', 'Корзина', 'Адрес', 'Связь']:
        builder.add(KeyboardButton(text=name))
    builder.adjust(2)
    #answer
    await message.answer_photo(photo=FSInputFile('./source/img/Welcome_Image.png'),
        caption= 'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ', 
        reply_markup=builder.as_markup(resize_keyboard=True, input_field_placeholder='Главное Меню'))

@router.message(Text(text='Связь'))
async def contact_us_menu(message: Message):
    
    #InlineKeyboard setup
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='coder: Alexkandr', url='t.me/alexkandr'),
        InlineKeyboardButton(text='designer: Moonylofly ', url='t.me/moonylofly')
    )
    
    #answer
    await message.answer_photo(photo=FSInputFile('./source/img/Contacts.png'),
        caption= 'Что-то не нравится - отсоси ^_^ \n Нахваливать только сообщениями от 1000 символов',
        reply_markup=builder.as_markup(resize_keyboard=True))