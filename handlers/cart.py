from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from db.postgre import postgredb
from db.redis import redisdb
from models.CartCallBackFactory import CartCallbackFactory
from keyboards.keyboards import cart_keyboard, item_in_cart_keyboard, addresses_keyboard
from aiogram.fsm.context import FSMContext
from models.purchaseFSM import PurchaseState

router = Router()

cart_message = 'Чего-то не хватает? \n Жми -> /catalog'

@router.message(Text(text='Корзина'))
async def cart_menu(message : Message):
    
    cart = redisdb.get_cart(message.from_user.id)
    #check cart
    if cart == {}:
        await message.answer_photo( photo=postgredb.image_by_name('Empty_cart'), caption=cart_message)
        return 

    #answer
    await message.answer_photo(photo=postgredb.image_by_name('Cart'),
        caption=cart_message,
        reply_markup=cart_keyboard(cart, message.from_user.id))

@router.callback_query(CartCallbackFactory.filter())
async def cart_action(call : CallbackQuery, callback_data : CartCallbackFactory, state : FSMContext):
    match callback_data.action:
        case 'clear':
            redisdb.clear_cart(callback_data.user_id)
            await call.message.edit_reply_markup(reply_markup=None)
            await call.answer(text='Корзина очищена', show_alert=True)
        case 'buy':
            await state.set_state(PurchaseState.ChooseAddress)
            await call.message.answer_photo(
                photo=postgredb.image_by_name('Address'),
                caption='Выберите адрес доставки', 
                reply_markup=addresses_keyboard(postgredb.get_addresses_by_user_id(callback_data.user_id)))
            await call.answer()
        case 'info':
            item = postgredb.select_by_id(callback_data.item_id)
            await call.message.edit_caption(caption=item.message_info())
            await call.message.edit_reply_markup(item_in_cart_keyboard(amount=callback_data.amount, item_id=callback_data.item_id, user_id=callback_data.user_id))
            await  call.answer()
        case 'save':
            new_cart = redisdb.change_amount(user_id=callback_data.user_id, item_id=callback_data.item_id, amount=callback_data.amount)
            await call.message.edit_caption(caption=cart_message)
            await call.message.edit_reply_markup(cart_keyboard(cart=new_cart, user_id=callback_data.user_id))
            await  call.answer()
        case 'delete':
            new_cart = redisdb.remove_item(user_id=callback_data.user_id, item_id=callback_data.item_id)
            await call.message.edit_caption(caption=cart_message)
            await call.message.edit_reply_markup(cart_keyboard(cart=new_cart, user_id=callback_data.user_id))
            await  call.answer()
        case 'decr':
            await call.message.edit_reply_markup(item_in_cart_keyboard(amount=callback_data.amount - 1, item_id=callback_data.item_id, user_id=callback_data.user_id))
            await  call.answer()
        case 'incr':
            await call.message.edit_reply_markup(item_in_cart_keyboard(amount=callback_data.amount + 1, item_id=callback_data.item_id, user_id=callback_data.user_id))
            await  call.answer()