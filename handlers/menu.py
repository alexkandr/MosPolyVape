from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from models.keyboards import MenuKeyboards
from models.db import images_tab


router = Router()

@router.message(Command(commands=["start"]))
async def start(message : Message):
    m = await message.answer_photo(photo=await images_tab.get_by_name('Welcome'),
        caption=f'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ', 
        reply_markup=MenuKeyboards.get_menu())

@router.message(Text(text='Связь'))
async def contact_us_menu(message: Message):
    
    await message.answer_photo(photo=await images_tab.get_by_name('Contacts'),
        caption= 'Что-то не нравится - отсоси ^_^ \n Нахваливать только сообщениями от 1000 символов',
        reply_markup=MenuKeyboards.get_contacts())

@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=MenuKeyboards.get_menu()
    )
