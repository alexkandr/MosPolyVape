from os import getenv
import re

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from models.dao import OrderDAO, ParilkaDAO
from models.fsm import ItemState, GiveIdState
from models.db import sklad_tab, images_tab, orders_tab

router = Router()

ADMIN_CHAT_ID = int(getenv('ADMIN_CHAT_ID')) if (getenv('ADMIN_CHAT_ID') is not None) else int(open('tokens.txt', 'r').readlines()[-1])
ADMIN_CHAT_ID = [ADMIN_CHAT_ID]

@router.message(Command(commands=['add']), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_item(message : Message, state : FSMContext):
    names = await sklad_tab.get_names()
    m = ''
    for item in names:
        m = m + f"{item['name']} /add_{item['id']} \n"
    m = m + '\n /add_new'
    await message.answer(text=m)



 #Add existing item

@router.message(Command(re.compile(r'add_\d+')), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_exist_item(message : Message,command : CommandObject, state : FSMContext):
    item_id = command.regexp_match.string.split('_')[1]
    await state.set_state(ItemState.add_amount)
    await state.update_data(item_id= item_id)
    await message.reply(text='Сколько добавить')

@router.message(F.text.regexp(r"^(\d+)$").as_("amount"), ItemState.add_amount, F.chat.id.in_(ADMIN_CHAT_ID))
async def add_amount(message : Message, state : FSMContext, amount : re.Match[str]):
    amount = int(amount.string)
    await sklad_tab.add_amount(id= (await state.get_data())['item_id'], amount=amount)
    await state.clear()
    await message.reply(text='Добавил')

@router.message(ItemState.add_amount ,F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_amount(message : Message):
    await message.reply(text='Ошибка')



#Adding new item

@router.message(Command(commands=['add_new']), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_new_item(message : Message, state : FSMContext):
    await state.set_state(ItemState.name)
    await message.reply(text='Название')

@router.message(ItemState.name, F.chat.id.in_(ADMIN_CHAT_ID))
async def name(message : Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(ItemState.description)
    await message.reply(text='Ок, описание:')

@router.message(ItemState.description, F.chat.id.in_(ADMIN_CHAT_ID))
async def description(message : Message, state : FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(ItemState.image)
    await message.reply(text=f"Ок, скинь {html.strikethrough('жопу')} картинку")

@router.message(ItemState.image, F.chat.id.in_(ADMIN_CHAT_ID), F.photo)
async def image(message : Message, state : FSMContext):
    await state.update_data(image = message.photo[-1].file_id)
    await state.set_state(ItemState.taste)
    await message.reply(text='Ок, вкус:')

@router.message(ItemState.image, F.chat.id.in_(ADMIN_CHAT_ID))
async def image(message : Message, state : FSMContext):
    await message.reply(text='Надо скинуть картинку русским языком же написано')

@router.message(ItemState.taste, F.chat.id.in_(ADMIN_CHAT_ID))
async def taste(message : Message, state : FSMContext):
    await state.update_data(taste = message.text)
    await state.set_state(ItemState.puffs)
    await message.reply(text='Ок, сколько тяжек:')

@router.message(F.text.regexp(r"^(\d+)$").as_("puffs"), ItemState.puffs, F.chat.id.in_(ADMIN_CHAT_ID))
async def puffs(message : Message, state : FSMContext, puffs : re.Match[str]):
    puffs = int(puffs.string)
    await state.update_data(puffs = puffs)
    await state.set_state(ItemState.price)
    await message.reply(text='Ок, сколько стоит:')

@router.message(ItemState.puffs, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_puffs(message : Message, state : FSMContext):
    await message.reply(text='ошибка')

@router.message(F.text.regexp(r"^(\d+)$").as_("price"), ItemState.price, F.chat.id.in_(ADMIN_CHAT_ID))
async def price(message : Message, state : FSMContext, price : re.Match[str]):
    price = int(price.string)
    await state.update_data(price = price)
    await state.set_state(ItemState.avaible)
    await message.reply(text='Ок, сколько добавить:')

@router.message(ItemState.price, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_price(message : Message, state : FSMContext):
    await message.reply(text='ошибка')

@router.message(F.text.regexp(r"^(\d+)$").as_("avaible"), ItemState.avaible, F.chat.id.in_(ADMIN_CHAT_ID))
async def avaible(message : Message, state : FSMContext, avaible : re.Match[str]):
    avaible = int(avaible.string)
    data = await state.get_data()
    item = ParilkaDAO(name=data['name'], description=data['description'], image=data['image'], taste=data['taste'], puffs=data['puffs'], price=data['price'], avaible=avaible)
    await sklad_tab.add(item=item)
    await message.reply(text='Ок, сохранил')

@router.message(ItemState.avaible, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_avaible(message : Message, state : FSMContext):
    await message.reply(text='ошибка')



#delete item
    
@router.message(Command(commands=['delete']), F.chat.id.in_(ADMIN_CHAT_ID))
async def delete_item(message : Message, state : FSMContext):
    names = await sklad_tab.get_names()
    m = ''
    for item in names:
        m = m + f"{item['name']} /delete_{item['id']} \n"
    await message.answer(text=m)



@router.message(Command(re.compile(r'delete_\d+')), F.chat.id.in_(ADMIN_CHAT_ID))
async def delete_item_id(message : Message,command : CommandObject):
    item_id = command.regexp_match.string.split('_')[1]
    await sklad_tab.delete_by_id(item_id)
    await message.reply(text='Удалено')

#save new image to db

@router.message(Command(commands=['save_image']), F.chat.id.in_(ADMIN_CHAT_ID))
async def save_image(message : Message, state : FSMContext):
    await state.set_state(GiveIdState.recieve_image)
    await message.answer(text=f'Жду картинку, с подписью (названием файла)')

@router.message(GiveIdState.recieve_image, F.photo, F.chat.id.in_(ADMIN_CHAT_ID))
async def get_image_ig(message : Message, state : FSMContext):
    await images_tab.add(file_id=message.photo[-1].file_id, file_name=message.caption)
    await state.clear()
    await message.answer(text=f'Сохранил')
    

@router.message(GiveIdState.recieve_image, F.chat.id.in_(ADMIN_CHAT_ID))
async def wrong_image_to_save(message : Message, state : FSMContext):
    await message.answer(text='Надо отправить картинку')



#delete image from db

@router.message(Command(commands=['delete_image']), F.chat.id.in_(ADMIN_CHAT_ID))
async def delete_image(message : Message, state : FSMContext):
    images = await images_tab.get_all()
    m = ''
    for img in images:
        m = m + f"{img['file_name']} /delete_image_{img['id']} \n"
    await message.answer(text=m)



@router.message(Command(re.compile(r'delete_image_\d+')), F.chat.id.in_(ADMIN_CHAT_ID))
async def add_exist_item(message : Message,command : CommandObject):
    img_id = command.regexp_match.string.split('_')[-1]
    await images_tab.delete(img_id)
    await message.reply(text='Удалено')

@router.message(Command(re.compile(r'orders[_w+\b]?')), F.chat.id.in_(ADMIN_CHAT_ID))
async def list_orders(message : Message, command : CommandObject):
    filter = command.regexp_match.string.split('_')[-1]
    filter = filter if filter!= 'orders' else ''
    reply = 'id  | сумма |   статус   | Время создания'
    for order in await orders_tab.get_all(filter):
        reply+= order_to_str(order)
    await message.answer(text=reply)

def order_to_str(order : OrderDAO) -> str:
    return f"\n{str(order.id).ljust(4)} | {str(order.total_sum).rjust(6)} | {order.status.center(10)} | {order.creating_time.strftime('%d/%m/%y %I:%M').ljust(14)}"