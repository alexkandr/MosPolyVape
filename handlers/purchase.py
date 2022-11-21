from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import  CallbackQuery
from aiogram.fsm.context import FSMContext

from models.keyboards import PurchaseKeyboards
from models.fsm import PurchaseState
from models.dao import OrderDAO
from models.db import cart_rep, orders_tab, ordered_items_tab, addresses_tab, sklad_tab
from handlers.admin import ADMIN_CHAT_ID


router = Router()


@router.callback_query(PurchaseState.PaymentMethod)
async def payment_method(call : CallbackQuery, state : FSMContext):
    match call.data:
        case 'cash':
            await state.update_data(payment_method='cash')
            await state.set_state(PurchaseState.Accept)
            await state.update_data(order=await AcceptanceForm(call=call, state=state))
        case 'transfer':
            await state.update_data(payment_method='transfer')
            await state.set_state(PurchaseState.Accept)
            await state.update_data(order=await AcceptanceForm(call=call, state=state))
        case 'SBP':
            pass
        case 'cancel':
            await state.clear()

    await call.message.delete()
    await call.answer()

@router.callback_query(PurchaseState.Accept)
async def accept(call : CallbackQuery, state : FSMContext):
    match call.data:
        case 'Accept':
            order = (await state.get_data())['order']
            order_id = await orders_tab.add(order)
            cart = await cart_rep.get_cart(call.from_user.id)
            await ordered_items_tab.add_cart(cart, order_id)
            await cart_rep.clear_cart(call.from_user.id)
            await state.clear()
            await SendMessage(chat_id=ADMIN_CHAT_ID[0], 
            text=f'''Поступил новый заказ номер {order_id} на сумму {order.total_sum}
    Для большей информации /order_{order_id}''')
            await call.message.answer('Ваш заказ сохранён и скоро будет доставлен')
        case _:
            await state.clear()
            await call.message.answer(text='что теперб?')
    
    await call.answer()

async def AcceptanceForm(call : CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address = await addresses_tab.get_by_id(data['chosen_address'])
    purchases = await cart_to_str(await cart_rep.get_cart(call.from_user.id))
    await call.message.answer(
        text=f'''Давай всё проверим:
        Адрес: 
            Общежитие №{address['obshaga']}, комната {address['room_number']}
        Товары:{purchases[0]}
        Всего:
            {purchases[1]} рублей
        Способ оплаты:
            {data['payment_method']}''',
        reply_markup=PurchaseKeyboards.get_acceptance_form()
    )
    return OrderDAO(user_id=call.from_user.id, address_id=data['chosen_address'], total_sum=purchases[1], payment_method=data['payment_method'])

async def cart_to_str(cart : dict):
    purchases = ''
    sum = 0
    for id, amount in cart.items():
        item = await sklad_tab.get_by_id(id)
        purchases += f"\n{' '*12}{item.name} : {amount} штук по {item.price}руб"
        sum += item.price*int(amount)
    return (purchases, sum)


