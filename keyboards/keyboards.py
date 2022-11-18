from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from models.addressCallBackFactory import AddressCallbackFactory
from models.ItemCallbackFactory import ItemCallbackFactory
from models.CartCallBackFactory import CartCallbackFactory
from db.postgre import postgredb



#Address.py

def obshaga_keyboard(obshagas : list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for o in obshagas:
        builder.button(text=o)
    builder.adjust(4)
    builder.button(text='отмена')
    return builder.as_markup(resize_keyboard=True)

def cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='отмена')
    return builder.as_markup(resize_keyboard=True)

def addresses_keyboard(addresses : list[dict], remove : bool = False) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    for i, address in enumerate(addresses): 
        builder.button(text= dict_to_str(address), callback_data=AddressCallbackFactory(action='address', address_index=i, address_id=address['id']))   
    
    if remove == True:
        builder.button(text='Отмена', callback_data=AddressCallbackFactory(action='cancel', address_index=None))
        builder.adjust(1)
        return builder.as_markup()
    builder.button(text='Добавить', callback_data=AddressCallbackFactory(action='add', address_index=None))
    if addresses != []:
        builder.button(text='Удалить', callback_data=AddressCallbackFactory(action='remove', address_index=None))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=False)

def dict_to_str(address : dict) -> str:
    return f'Общежитие {str(address["obshaga"])}, комната {str(address["room_number"])}'

def payment_method() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Наличными при получении', callback_data='cash')
    builder.button(text='Переводом при получении', callback_data='transfer')
    builder.button(text='Отмена', callback_data='cancel')
    builder.adjust(1)
    return builder.as_markup()


#Menu.py

def menu_keyboard() -> ReplyKeyboardMarkup:
    
    builder = ReplyKeyboardBuilder()    
    for name in ['Каталог', 'Корзина', 'Адрес', 'Связь']:
        builder.add(KeyboardButton(text=name))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def contactus_keyboard() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.button(text='coder: Alexkandr', url='t.me/alexkandr')
    builder.button(text='designer: Moonylofly ', url='t.me/moonylofly')

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)



#Catalog.py

def catalog_keyboard() -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    
    builder.button(text='До 1000 затяжек', callback_data='catalog_lt1000')
    builder.button(text='1000 - 2000 затяжек', callback_data='catalog_lt2000')
    builder.button(text='2000 - 4000 затяжек', callback_data='catalog_lt4000')
    builder.button(text='4000+ затяжек', callback_data='catalog_gt4000')
    
    builder.adjust(1)

    return builder.as_markup()

def item_keyboard(amount : int, item_id : int) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    
    builder.button(text="-1", callback_data=ItemCallbackFactory(action='decr', amount=amount, item_id=item_id))
    builder.button(text=str(amount), callback_data=ItemCallbackFactory(action='none', amount=amount, item_id=item_id))
    builder.button(text="+1", callback_data=ItemCallbackFactory(action='incr', amount=amount, item_id=item_id))
    
    builder.button(text='В корзину', callback_data=ItemCallbackFactory(action='to_cart', amount=amount, item_id=item_id))
    
    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True)


#cart.py

def cart_keyboard(cart : dict, user_id : int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if cart == {}:
        return builder.as_markup()

    sum = 0
    for id, amount in cart.items():
        item = postgredb.select_by_id(id)
        t_price = item.price * int(amount)
        builder.button(text=f'{item.name.ljust(10)} {amount}шт * {item.price}руб = {t_price}руб', 
            callback_data=CartCallbackFactory(action='info', user_id=user_id, item_id=item.id, amount=amount))
        sum += t_price
    
    builder.button(text='Очистить Корзину', callback_data=CartCallbackFactory(action='clear', user_id=user_id))
    builder.button(text=f'Купить всё за {sum}руб', callback_data=CartCallbackFactory(action='buy', user_id=user_id))

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def item_in_cart_keyboard(amount : int, item_id : int, user_id : int) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    
    builder.button(text="-1", callback_data=CartCallbackFactory(action='decr', user_id=user_id, amount=amount, item_id=item_id))
    builder.button(text=str(amount), callback_data=CartCallbackFactory(action='none', user_id=user_id, amount=amount, item_id=item_id))
    builder.button(text="+1", callback_data=CartCallbackFactory(action='incr', user_id=user_id, amount=amount, item_id=item_id))
    
    builder.button(text='Удалить из корзины', callback_data=CartCallbackFactory(action='delete', user_id=user_id, amount=amount, item_id=item_id))
    builder.adjust(3)
    builder.button(text='Сохранить', callback_data=CartCallbackFactory(action='save', user_id=user_id, amount=amount, item_id=item_id))

    return builder.as_markup(resize_keyboard=True)



#purchase.py

def acceptance_form() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Подтверждаю заказ', callback_data='Accept')
    builder.button(text='Изменить заказ', callback_data='change')
    builder.adjust(1)
    return builder.as_markup()
