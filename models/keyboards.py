from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from models.callback_factory import AddressCallbackFactory, ItemCallbackFactory, CartCallbackFactory
from models.db import sklad_tab


class AddressKeyboards:
    
    @staticmethod
    def list_obshagas(obshagas : list[str]) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for o in obshagas:
            builder.button(text=o)
        builder.adjust(4)
        builder.button(text='отмена')
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def list_addresses(addresses : list[dict], remove : bool = False) -> InlineKeyboardMarkup:
        def dict_to_str(address : dict) -> str:
            return f'Общежитие {str(address["obshaga"])}, комната {str(address["room_number"])}'

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

    @staticmethod
    def list_payment_method() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='Наличными при получении', callback_data='cash')
        builder.button(text='Переводом при получении', callback_data='transfer')
        builder.button(text='Отмена', callback_data='cancel')
        builder.adjust(1)
        return builder.as_markup()



class MenuKeyboards:

    @staticmethod 
    def get_menu() -> ReplyKeyboardMarkup:
        
        builder = ReplyKeyboardBuilder()    
        for name in ['Каталог', 'Корзина', 'Адрес', 'Связь']:
            builder.add(KeyboardButton(text=name))
        builder.adjust(2)

        return builder.as_markup(resize_keyboard=True)

    @staticmethod 
    def get_contacts() -> InlineKeyboardMarkup:

        builder = InlineKeyboardBuilder()
        builder.button(text='coder: Alexkandr', url='t.me/alexkandr')
        builder.button(text='designer: Moonylofly ', url='t.me/moonylofly')

        builder.adjust(2)

        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def show_cancel_button() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='отмена')
        return builder.as_markup(resize_keyboard=True)


class CatalogKeyboards:

    @staticmethod
    def list_categories() -> InlineKeyboardMarkup:
        
        builder = InlineKeyboardBuilder()
        
        builder.button(text='До 1000 затяжек', callback_data='catalog_lt1000')
        builder.button(text='1000 - 2000 затяжек', callback_data='catalog_lt2000')
        builder.button(text='2000 - 4000 затяжек', callback_data='catalog_lt4000')
        builder.button(text='4000+ затяжек', callback_data='catalog_gt4000')
        
        builder.adjust(1)

        return builder.as_markup()

    @staticmethod 
    def show_item(amount : int, item_id : int) -> InlineKeyboardMarkup:
        
        builder = InlineKeyboardBuilder()
        
        builder.button(text="-1", callback_data=ItemCallbackFactory(action='decr', amount=amount, item_id=item_id))
        builder.button(text=str(amount), callback_data=ItemCallbackFactory(action='none', amount=amount, item_id=item_id))
        builder.button(text="+1", callback_data=ItemCallbackFactory(action='incr', amount=amount, item_id=item_id))
        
        builder.button(text='В корзину', callback_data=ItemCallbackFactory(action='to_cart', amount=amount, item_id=item_id))
        
        builder.adjust(3)

        return builder.as_markup(resize_keyboard=True)


class CartKeyboards:

    @staticmethod 
    async def get_cart(cart : dict, user_id : int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if cart == {}:
            
            return builder.as_markup()

        sum = 0
        for id, amount in cart.items():
            item = await sklad_tab.get_by_id(id)
            t_price = item.price * int(amount)
            builder.button(text=f'{item.name.ljust(10)} {amount}шт * {item.price}руб = {t_price}руб', 
                callback_data=CartCallbackFactory(action='info', user_id=user_id, item_id=item.id, amount=amount))
            sum += t_price
        
        builder.button(text='Очистить Корзину', callback_data=CartCallbackFactory(action='clear', user_id=user_id))
        builder.button(text=f'Купить всё за {sum}руб', callback_data=CartCallbackFactory(action='buy', user_id=user_id))

        builder.adjust(1)

        return builder.as_markup(resize_keyboard=True)


    @staticmethod 
    def show_item(amount : int, item_id : int, user_id : int) -> InlineKeyboardMarkup:
        
        builder = InlineKeyboardBuilder()
        
        builder.button(text="-1", callback_data=CartCallbackFactory(action='decr', user_id=user_id, amount=amount, item_id=item_id))
        builder.button(text=str(amount), callback_data=CartCallbackFactory(action='none', user_id=user_id, amount=amount, item_id=item_id))
        builder.button(text="+1", callback_data=CartCallbackFactory(action='incr', user_id=user_id, amount=amount, item_id=item_id))
        
        builder.button(text='Удалить из корзины', callback_data=CartCallbackFactory(action='delete', user_id=user_id, amount=amount, item_id=item_id))
        builder.adjust(3)
        builder.button(text='Сохранить', callback_data=CartCallbackFactory(action='save', user_id=user_id, amount=amount, item_id=item_id))

        return builder.as_markup(resize_keyboard=True)



class PurchaseKeyboards:

    @staticmethod 
    def get_acceptance_form() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='Подтверждаю заказ', callback_data='Accept')
        builder.button(text='Изменить заказ', callback_data='change')
        builder.adjust(1)
        return builder.as_markup()
