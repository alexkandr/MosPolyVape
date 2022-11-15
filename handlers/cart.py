from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from db.postgre import postgredb
from db.redis import redisdb
from models.CartCallBackFactory import CartCallbackFactory
from keyboards.keyboards import cart_to_inline_markup, item_keyboard

router = Router()


@router.message(Text(text='Корзина'))
async def cart_menu(message : Message):
    
    cart = redisdb.get_cart(message.from_user.id)
    #check cart
    if cart == {}:
        await message.answer_photo( photo=postgredb.image_by_name('Empty_cart'))
        return 

    #answer
    await message.answer_photo(photo=postgredb.image_by_name('Cart'),
        reply_markup=cart_to_inline_markup(cart, message.from_user.id))

@router.callback_query(CartCallbackFactory.filter())
async def cart_action(call : CallbackQuery, callback_data : CartCallbackFactory):
    match callback_data.action:
        case 'clear':
            redisdb.clear_cart(callback_data.user_id)
            await call.answer(text='', show_alert=True)
        case 'buy':
            order = redisdb.clear_cart(callback_data.user_id)
            await call.answer()
        case 'info':
            await  call.answer()
    
    await call.message.edit_reply_markup(reply_markup=cart_to_inline_markup(redisdb.get_cart(call.from_user.id), call.from_user.id))
        