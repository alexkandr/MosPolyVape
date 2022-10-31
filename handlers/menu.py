from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile
from keyboards.keyboards import menu_keyboard, contactus_keyboard
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

router = Router()
@router.message(Command(commands=["start"]))
async def start(message : Message):
    
    m = await message.answer_photo(photo=FSInputFile('./source/img/Welcome_Image.png'),
        caption= f'Это бот для покупки парилок в общаге. feel free to contact us^ enjoy the ПЫХ {message.chat.id}', 
        reply_markup= menu_keyboard())
    print(m.from_user.id)    

@router.message(Text(text='Связь'))
async def contact_us_menu(message: Message):
    
    await message.answer_photo(photo=FSInputFile('./source/img/Contacts.png'),
        caption= 'Что-то не нравится - отсоси ^_^ \n Нахваливать только сообщениями от 1000 символов',
        reply_markup=contactus_keyboard())

@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=menu_keyboard()
    )
