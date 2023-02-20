import os

import requests
from dotenv import load_dotenv

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import (Bot,
                     Dispatcher,
                     executor,
                     types)

from utils import OrderStateGroup
from quires_tools import (verification_access,
                          make_new_order,
                          send_secretkey)

from markups_client_bot import (main_menu,
                                payment_menu,
                                secret_menu,
                                contactus_menu,
                                executor_menu)


load_dotenv()
telegram_client_token = os.getenv('TELEGRAM_CLIENT_TOKEN')
telegram_executor_token = os.getenv('TELEGRAM_EXECUTOR_TOKEN')
storage = MemoryStorage()
bot2 = Bot(token=telegram_executor_token)
bot = Bot(token=telegram_client_token)
dp = Dispatcher(bot, bot2, storage=storage)


@dp.message_handler(commands=['start'])
async def verification_user(message: types.Message) -> None:
    try:
        tg_username, dp_user_id, tg_user_id = verification_access(message)
        order_description['tg_username'] = tg_username
        order_description['dp_user_id'] = dp_user_id
        order_description['tg_user_id'] = tg_user_id
        await message.answer(
            f'Добро пожаловать {message.from_user.first_name}!\n\n'
            'Этот бот принимает Ваши заявки и передаёт '
            'их исполнителю.\n\n'
            'Если готовы сделать заказ нажмите:\n'
            '"📑Оформить новый заказ"',
            reply_markup=main_menu
        )
    except (TypeError, requests.HTTPError):
        await message.answer(
            f'Приветствую, {message.from_user.first_name}\n\n'
            '🚧 Данный бот 🤖 работает, как подписочный сервис,'
            ' к сожалению вы не были найдены среди авторизованных '
            'пользователей 🚧\n\n '
            '👇<b>Получить</b> доступ можно, нажав на кнопку ниже👇',
            parse_mode='HTML',
            reply_markup=payment_menu
        )


@dp.callback_query_handler(text='new_order')
async def wait_order(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        '❓Как оформляется заказ❓\n\n'
        'Напишите его в свободной форме.\n\n'
        'Например так:\n'
        '<i>Здравствуйте, нужно загрузить 450 SKU '
        'на сайт из Execel таблицы</i>\n\n'
        '<b>💬Следующее Ваше сообщение улетит исполнителю.</b>\n'
        '',
        parse_mode='HTML'
    )
    await OrderStateGroup.new_order.set()


@dp.message_handler(content_types=['text'], state=OrderStateGroup.new_order)
async def make_order(message: types.Message, state: FSMContext):
    async with state.proxy() as new_order:
        new_order["text"] = message.text
        order_id = make_new_order(new_order, order_description)
        order_description['order_id'] = order_id
    await state.finish()
    await message.answer(
        f'{message.from_user.first_name}, чтобы исполнитель мог начать работу.'
        '\nЕму понадобиться доступ🔐\n\n'
        'Напишите исполнителю как попасть на сайт👇\n\n',
        parse_mode='HTML',
        reply_markup=secret_menu
    )


@dp.callback_query_handler(text='secret_key')
async def wait_order(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        '⚠️После исполнения заказа рекомендуем поменять данные для входа⚠️\n\n'
        '<b>💬Следующее Ваше сообщение улетит исполнителю.</b>\n',
        parse_mode='HTML'
    )
    await OrderStateGroup.secretkey.set()


@dp.message_handler(content_types=['text'], state=OrderStateGroup.secretkey)
async def take_order(message: types.Message, state: FSMContext):
    async with state.proxy() as order:
        order["secret"] = message.text
        send_secretkey(order, order_description)
        await state.finish()
    await message.answer(
        "Ваш заказ принят!✅\n\n"
        "<i>\nЕсли у исполнителя возникнут "
        "вопросы он Вам напишет </i>",
        parse_mode="HTML",
        reply_markup=contactus_menu
    )


@dp.callback_query_handler(text='comment_to')
async def comment_to_client(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "💬 Ваше следующее сообщение "
                           "будет отправлено клиенту")
    await OrderStateGroup.comment_to.set()


@dp.message_handler(content_types=['text'], state=OrderStateGroup.comment_to)
async def worker_comment(message: types.Message, state: FSMContext):
    async with state.proxy():
        client_tg_id = "406682076"
        await bot2.send_message(
            client_tg_id,
            'Здравствуйте, наш специалист собирается взяться за вашу заявку, '
            'но у него возникли вопросы.\n\n'
            '❓ <b>Вопрос звучит так:</b>\n'
            f'<i>"{message.text}"</i>\n\n'
            'Ответить вы можете через соответствующий функционал ниже',
                               parse_mode='HTML', reply_markup=executor_menu)
        await bot.send_message(
            message.from_user.id,
            'Сообщение было отправлено исполнителю...')
    await state.finish()


@dp.message_handler(content_types="text")
async def contact_us(message: types.Message):
    await message.reply(
        "Я молодой бот, и ещё только учусь.👨‍🎓\n"
        "И не знаю как отреагировать на это.\n"
        "Напишите моему человеку - он поможет.\n",
        reply_markup=contactus_menu
    )


@dp.callback_query_handler()
async def answer_callback(callback: types.CallbackQuery):
    if callback.data == "answers":
        await callback.message.answer(
            text="Чтобы ответить на порос инсполнителя нажмите:\n"
                 "📬Ответить на вопросы исполнителя")


if __name__ == '__main__':
    order_description = {}
    executor.start_polling(dp, skip_updates=True)
