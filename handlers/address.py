import random
from re import Match

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text

from models.db import addresses_tab, images_tab
from models.fsm import AddressState, PurchaseState
from models.callback_factory import AddressCallbackFactory
from models.keyboards import AddressKeyboards, MenuKeyboards

router = Router()
obshagas = ['4']


#Menu message handler
###################################

@router.message(Text(text= 'Адрес'))
async def address_menu(message : Message):
    
    #Check Address
    addresses = await addresses_tab.get_by_user_id(message.from_user.id)
    if addresses == []:
        caption = 'Здесь пока ничего нет'
    else:
        caption = 'Ваши адреса:'

    #answer
    await message.answer_photo( photo=FSInputFile('./source/img/Address.png'),
        caption=caption,
        reply_markup=AddressKeyboards.list_addresses(addresses))



#Remove callbak handler
###################################        

@router.callback_query(AddressState.delete_address, AddressCallbackFactory.filter())
async def chosen_address_to_delete(call : CallbackQuery, callback_data : AddressCallbackFactory, state : FSMContext):
    match callback_data.action:
        
        case 'address':
            addresses = await addresses_tab.get_by_id(call.from_user.id)
            address = addresses[callback_data.address_index]
            await addresses_tab.delete(user_id=call.from_user.id, obshaga=address['obshaga'], room_number=address['room_number'])

        case _:
            pass
    
    result_addresses = await addresses_tab.get_by_id(call.from_user.id)

    await call.message.edit_caption(
        caption= 'Здесь пока ничего нет' if result_addresses == [] else 'Ваши адреса:',
        reply_markup=AddressKeyboards.list_addresses(result_addresses)
        )

    await state.clear()
    await call.answer()



#Menu callback handler
####################################

@router.callback_query(AddressCallbackFactory.filter())
async def will_to_change_address(call : CallbackQuery, callback_data : AddressCallbackFactory , state : FSMContext) :

    match callback_data.action:
        case 'address':
            if (await state.get_state()) == PurchaseState.ChooseAddress:
                await state.set_state(PurchaseState.PaymentMethod)
                await state.update_data(chosen_address = callback_data.address_id)
                await call.message.answer_photo(photo=await images_tab.get_by_name('Payment_method'),
                    caption='', reply_markup=AddressKeyboards.list_payment_method())
                await call.message.delete()  

        case 'remove':
            await state.set_state(AddressState.delete_address)
            await call.message.edit_caption(caption= 'Выберите адрес который хотите удалить',
                reply_markup=AddressKeyboards.list_addresses(await addresses_tab.get_by_user_id(call.from_user.id), 
                remove=True))

        case 'add':
            await state.set_state(AddressState.choose_obshaga)
            #await state.update_data(main_message = call.message, messages = [])
            await call.message.answer('Укажите номер общежития:', reply_markup=AddressKeyboards.list_obshagas(obshagas))
            #await call.message.edit_reply_markup(
            #    reply_markup=addresses_keyboard(await addresses_tab.get_addresses_by_user_id(call.from_user.id)))
    await call.answer()



#Add obshaga message handler
###################################

@router.message(AddressState.choose_obshaga, F.text.in_(obshagas))
async def add_obshaga(message : Message, state : FSMContext):
    await state.update_data(obshaga = int(message.text))
    await message.reply('Принято, теперь укажите комнату', reply_markup=MenuKeyboards.show_cancel_button())
    await state.set_state(AddressState.choose_room)

@router.message(AddressState.choose_obshaga)
async def wrong_obshaga(message : Message):
    await message.reply(random.choice(['Сюда мы эээ... не доставляем', 'русским по белому же написаны доступные номера...', 'просто... попробуй ещё...', 'НЕВЕРНЫЙ ВВОД ПОВТОРИТЕ ПОПЫТКУ']))



#Add room number message handler
###################################

@router.message(AddressState.choose_room, F.text.regexp(r"^(\d+)$").as_("digits"))
async def add_room(message : Message, state : FSMContext, digits : Match[str]):
    room_number = int(digits.string)
    if room_number > 0 and room_number < 400:

        await addresses_tab.add(user_id=message.from_user.id, 
            obshaga= (await state.get_data())['obshaga'], room_number=room_number)

        await message.reply('Понятно, добавили', reply_markup=MenuKeyboards.get_menu())
        await state.clear()
        await address_menu(message)
        return
    await message.reply(random.choice(['Сюда мы эээ... не доставляем', 'я таких чисел не знаю', 'Это ж сколько до этой комнаты добираться... может ты ошибся? попробуй ещё', 'too much чел']))
    
    

@router.message(AddressState.choose_room)
async def wrong_room(message : Message): 
    await message.reply(random.choice(['Ошибся или по-приколу?', 'Специально же написано - номер', 'просто... попробуй ещё...', 'НЕВЕРНЫЙ ВВОД ПОВТОРИТЕ ПОПЫТКУ', 'не понял']))
