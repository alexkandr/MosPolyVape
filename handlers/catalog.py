from os import getenv
from aiogram import Router, html
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters import Text
from aiogram.types import FSInputFile, URLInputFile
from db.postgre import postgredb
from models.ItemCallbackFactory import ItemCallbackFactory

router = Router()

@router.message(Text(text='Каталог'))
async def catalog_menu(message : Message):
    
    #InlineKeyboard setup
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='До 1000 затяжек', callback_data='catalog_lt1000'),
        InlineKeyboardButton(text='1000 - 2000 затяжек', callback_data='catalog_lt2000'),
        InlineKeyboardButton(text='2000 - 4000 затяжек', callback_data='catalog_lt4000'),
        InlineKeyboardButton(text='4000+ затяжек', callback_data='catalog_gt4000')
    )
    builder.adjust(1)

    #answer
    await message.answer_photo(photo=FSInputFile('./source/img/Catalog.png'),
        reply_markup=builder.as_markup(resize_keyboard=True) )

@router.callback_query(Text(text_startswith='catalog_'))
async def show_catalog(call : CallbackQuery):
    
    #Choose appropriate items
    _filter = call.data.split('_')[1]
    showing_data = postgredb.select_by_puffs(_filter)
    
    #Check for empty
    if showing_data == []:
        await call.message.answer(text='Здесь пока ничего нет')
        await call.answer()
        return

    #Show items
    for item in showing_data:
        await call.message.answer_photo(photo= URLInputFile(item.image), caption=(item.message_info()),
        reply_markup= get_item_keyboard(0, item.id))

    await call.answer()

def get_item_keyboard(amount : int, item_id : int) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    
    builder.button(text="-1", callback_data=ItemCallbackFactory(action='decr', amount=amount, item_id=item_id))
    builder.button(text=str(amount), callback_data=ItemCallbackFactory(action='none', amount=amount, item_id=item_id))
    builder.button(text="+1", callback_data=ItemCallbackFactory(action='incr', amount=amount, item_id=item_id))
    
    builder.button(text='В корзину', callback_data=ItemCallbackFactory(action='to_cart', amount=amount, item_id=item_id))
    
    builder.adjust(3)

    return builder.as_markup()

async def update_item_markup(message: Message, new_amount : int, item_id : int):
    new_amount = new_amount if new_amount > 0 else 0
    await message.edit_reply_markup(reply_markup=get_item_keyboard(new_amount, item_id))

@router.callback_query(ItemCallbackFactory.filter())
async def callback_catalog(call : CallbackQuery, callback_data : ItemCallbackFactory):
    
    match callback_data.action:
        case 'decr':
            await update_item_markup(call.message, callback_data.amount - 1, callback_data.item_id)
        case 'incr':
            await update_item_markup(call.message, callback_data.amount + 1, callback_data.item_id)
        case 'none':
            pass
        case 'to_cart':
            await update_item_markup(call.message, 0, callback_data.item_id)
            await call.answer(text=f'в корзину добавлено {callback_data.amount} парилок', show_alert=True)
            return
    await call.answer()



