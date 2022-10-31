from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from models.give_idFSM import GiveIdState


CHAT_WITH_FEEDBACK_BOT_ID = -899075007
router = Router()

@router.message(Command(commands=['give_file_id']), F.chat.id == CHAT_WITH_FEEDBACK_BOT_ID)
async def give_file_id(message : Message, state : FSMContext):
    await state.set_state(GiveIdState.recieve_image)
    await message.answer(text=f'Жду картинку')

@router.message(GiveIdState.recieve_image, F.photo, F.chat.id == CHAT_WITH_FEEDBACK_BOT_ID)
async def derzhi_file_id(message : Message, state : FSMContext):
    await state.clear()
    await message.answer(text=f'Скопируй и отправь id ниже \n{message.photo[-1].file_id}')
    

@router.message(GiveIdState.recieve_image, F.chat.id == CHAT_WITH_FEEDBACK_BOT_ID)
async def derzhi_file_id(message : Message, state : FSMContext):
    await message.answer(text='Надо отправить картинку')
