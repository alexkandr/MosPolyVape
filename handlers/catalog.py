from aiogram import Router, html
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.types import FSInputFile
from db.postgre import postgredb
from models.ItemCallbackFactory import ItemCallbackFactory
from keyboards.keyboards import catalog_keyboard, item_keyboard

router = Router()

@router.message(Text(text='Каталог'))
async def catalog_menu(message : Message):
    
    await message.answer_photo(photo=FSInputFile('./source/img/Catalog.png'),
        reply_markup=catalog_keyboard() )

@router.callback_query(Text(startswith='catalog_'))
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
        await call.message.answer_photo(photo= item.image, caption=(item.message_info()),
        reply_markup= item_keyboard(0, item.id))

    await call.answer()

async def update_item_markup(message: Message, new_amount : int, item_id : int):
    new_amount = new_amount if new_amount > 0 else 0
    await message.edit_reply_markup(reply_markup=item_keyboard(new_amount, item_id))

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



