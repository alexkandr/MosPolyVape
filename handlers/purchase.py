from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import  CallbackQuery
from aiogram.fsm.context import FSMContext
from models.purchaseFSM import PurchaseState
from models.order import order
from db.postgre import postgredb
from db.redis import redisdb
from keyboards.keyboards import acceptance_form
from handlers.admin import ADMIN_CHAT_ID

router = Router()

@router.callback_query(PurchaseState.PaymentMethod)
async def payment_method(call : CallbackQuery, state : FSMContext):
    match call.data:
        case 'cash':
            await state.update_data(payment_method='cash')
            await state.set_state(PurchaseState.Accept)
            await state.update_data(order = await AcceptanceForm(call=call, state=state))
        case 'transfer':
            await state.update_data(payment_method='transfer')
            await state.set_state(PurchaseState.Accept)
            await state.update_data(order = await AcceptanceForm(call=call, state=state))
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
            order_id = postgredb.save_order(order)
            cart = redisdb.get_cart(call.from_user.id)
            postgredb.save_ordered_items(cart, order_id)
            redisdb.clear_cart(call.from_user.id)
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
    address = postgredb.get_address_by_id(data['chosen_address'])
    purchases = await cart_to_str(redisdb.get_cart(call.from_user.id))
    await call.message.answer(
        text=f'''Давай всё проверим:
        Адрес: 
            Общежитие №{address['obshaga']}, комната {address['room_number']}
        Товары:{purchases[0]}
        Всего:
            {purchases[1]} рублей
        Способ оплаты:
            {data['payment_method']}''',
        reply_markup=acceptance_form()
    )
    return order(user_id=call.from_user.id, address_id=data['chosen_address'], total_sum=purchases[1], payment_method=data['payment_method'])

async def cart_to_str(cart : dict):
    purchases = ''
    sum = 0
    for id, amount in cart.items():
        item = postgredb.select_by_id(id)
        purchases += f"\n{' '*12}{item.name} : {amount} штук по {item.price}руб"
        sum += item.price*int(amount)
    return (purchases, sum)


