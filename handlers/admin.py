from os import getenv
import re
from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from db.postgre import postgredb
from models.adminFSM import itemState
from models.give_idFSM import GiveIdState
from models.item import parilka

router = Router()

ADMIN_CHAT_ID = getenv('SPECIAL_CHATS') if (getenv('SPECIAL_CHATS') is not None) else open('tokens.txt', 'r').readlines()[2]


@router.message(Command(commands=['add']), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_item(message : Message, state : FSMContext):
    names = postgredb.select_all_names()
    m = ''
    for item in names:
        m = m + f"{item['name']} /add_{item['id']} \n"
    m = m + '\n /add_new'
    await message.answer(text=m)



 #Add existing item

@router.message(Command(re.compile(r'add_\d+')), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_exist_item(message : Message,command : CommandObject, state : FSMContext):
    item_id = command.regexp_match.string.split('_')[1]
    await state.set_state(itemState.add_amount)
    await state.update_data(item_id= item_id)
    await message.reply(text='Сколько добавить')

@router.message(F.text.regexp(r"^(\d+)$").as_("amount"), itemState.add_amount, F.chat.id.in_(ADMIN_CHAT_ID))
async def add_amount(message : Message, state : FSMContext, amount : re.Match[str]):
    amount = int(amount.string)
    postgredb.add_existing_parilkas(id= (await state.get_data())['item_id'], amount=amount)
    await state.clear()
    await message.reply(text='Добавил')

@router.message(itemState.add_amount ,F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_amount(message : Message):
    await message.reply(text='Ошибка')



#Adding new item

@router.message(Command(commands=['add_new']), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_new_item(message : Message, state : FSMContext):
    await state.set_state(itemState.name)
    await message.reply(text='Название')

@router.message(itemState.name, F.chat.id.in_(ADMIN_CHAT_ID))
async def name(message : Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(itemState.description)
    await message.reply(text='Ок, описание:')

@router.message(itemState.description, F.chat.id.in_(ADMIN_CHAT_ID))
async def description(message : Message, state : FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(itemState.image)
    await message.reply(text=f"Ок, скинь {html.strikethrough('жопу')} картинку")

@router.message(itemState.image, F.chat.id.in_(ADMIN_CHAT_ID), F.photo)
async def image(message : Message, state : FSMContext):
    await state.update_data(image = message.photo[-1].file_id)
    await state.set_state(itemState.taste)
    await message.reply(text='Ок, вкус:')

@router.message(itemState.taste, F.chat.id.in_(ADMIN_CHAT_ID))
async def taste(message : Message, state : FSMContext):
    await state.update_data(taste = message.text)
    await state.set_state(itemState.puffs)
    await message.reply(text='Ок, сколько тяжек:')

@router.message(F.text.regexp(r"^(\d+)$").as_("puffs"), itemState.puffs, F.chat.id.in_(ADMIN_CHAT_ID))
async def puffs(message : Message, state : FSMContext, puffs : re.Match[str]):
    puffs = int(puffs.string)
    await state.update_data(puffs = puffs)
    await state.set_state(itemState.price)
    await message.reply(text='Ок, сколько стоит:')

@router.message(itemState.puffs, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_puffs(message : Message, state : FSMContext):
    await message.reply(text='ошибка')

@router.message(F.text.regexp(r"^(\d+)$").as_("price"), itemState.price, F.chat.id.in_(ADMIN_CHAT_ID))
async def price(message : Message, state : FSMContext, price : re.Match[str]):
    price = int(price.string)
    await state.update_data(price = price)
    await state.set_state(itemState.avaible)
    await message.reply(text='Ок, сколько добавить:')

@router.message(itemState.price, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_price(message : Message, state : FSMContext):
    await message.reply(text='ошибка')

@router.message(F.text.regexp(r"^(\d+)$").as_("avaible"), itemState.avaible, F.chat.id.in_(ADMIN_CHAT_ID))
async def avaible(message : Message, state : FSMContext, avaible : re.Match[str]):
    avaible = int(avaible.string)
    data = await state.get_data()
    item = parilka(name=data['name'], description=data['description'], image=data['image'], taste=data['taste'], puffs=data['puffs'], price=data['price'], avaible=avaible)
    postgredb.add_new_parilkas(item=item)
    await message.reply(text='Ок, сохранил')

@router.message(itemState.avaible, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_avaible(message : Message, state : FSMContext):
    await message.reply(text='ошибка')



#delete item
    
@router.message(Command(commands=['delete']), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_item(message : Message, state : FSMContext):
    names = postgredb.select_all_names()
    m = ''
    for item in names:
        m = m + f"{item['name']} /delete_{item['id']} \n"
    m = m + '\n /add_new'
    await message.answer(text=m)



@router.message(Command(re.compile(r'delete_\d+')), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_exist_item(message : Message,command : CommandObject):
    item_id = command.regexp_match.string.split('_')[1]
    postgredb.delete_by_item_id(item_id)
    await message.reply(text='Удалено')

#give file id

@router.message(Command(commands=['give_file_id']), F.chat.id == ADMIN_CHAT_ID)
async def give_file_id(message : Message, state : FSMContext):
    await state.set_state(GiveIdState.recieve_image)
    await message.answer(text=f'Жду картинку')

@router.message(GiveIdState.recieve_image, F.photo, F.chat.id == ADMIN_CHAT_ID)
async def derzhi_file_id(message : Message, state : FSMContext):
    await state.clear()
    await message.answer(text=f'Вот твой id \n{message.photo[-1].file_id}')
    

@router.message(GiveIdState.recieve_image, F.chat.id == ADMIN_CHAT_ID)
async def derzhi_file_id(message : Message, state : FSMContext):
    await message.answer(text='Надо отправить картинку')