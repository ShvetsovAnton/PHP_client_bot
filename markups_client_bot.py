from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

# -- Payment menu --
payment_button = InlineKeyboardButton(
    '💰Оплатить подписку',
    url='httpss://stripe.com/docs/api'
)
payment_menu = InlineKeyboardMarkup().add(payment_button)

# -- Main menu --
order_button = InlineKeyboardButton(
    '📑Оформить новый заказ',
    callback_data='new_order'
)
contactus_button = InlineKeyboardButton(
    '💬Связать с нами',
    url='https://t.me/shvetsovantonm'
)
main_menu = InlineKeyboardMarkup().add(
    order_button,
    contactus_button
)

# --Secret keys menu--
secret_key_button = InlineKeyboardButton(
    '🕵️Отправить данные на вход',
    callback_data="secret_key"
)
secret_menu = InlineKeyboardMarkup().add(
    secret_key_button
)

# -- Contact us --

contactus_button = KeyboardButton(
    '💬Связать с нами',
    url='https://t.me/shvetsovantonm')
contactus_menu = InlineKeyboardMarkup().add(contactus_button)

# -- Answer to executor --
comment_to_order_button = KeyboardButton('📬Ответить на вопросы исполнителя')
contactus_button = KeyboardButton('💬Связать с нами')
executor_answer_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    comment_to_order_button,
    contactus_button
)

# # -- test button --
#
# test = InlineKeyboardButton("test", callback_data="test")
# test_menu = InlineKeyboardMarkup().add(test)


# -- Executor answer --

executor_answer = InlineKeyboardButton("comment_to",
                                       callback_data="comment_to")
executor_menu = InlineKeyboardMarkup().add(executor_answer)
