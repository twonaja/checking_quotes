from aiogram import Dispatcher
from aiogram import types
from aiogram import executor

import asyncio

from loader import do_job
from loader import read_config_file

from config import HELP_ME
from config import FILE_NAME
from config import INTERVAL
from config import USER_ID


def bin_bot(dp: Dispatcher, currencies_buttons: list):

    @dp.message_handler(commands='start')
    async def start(message: types.Message):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*currencies_buttons)
        await message.answer('Выберите интересующие вас валюты:', reply_markup=keyboard)

    @dp.message_handler(commands='help')
    async def help(message: types.Message):
        await message.answer(HELP_ME)

    @dp.message_handler(content_types=['text'])
    async def handle_text(message):
        currencies_dict = read_config_file(FILE_NAME)
        if message.text in currencies_buttons and message.text != 'FROM FILE':
            status_response = do_job(message.text, currencies_dict[message.text]['trigger'],
                                     currencies_dict[message.text]['price'])
            if status_response != 'None':
                await message.answer(status_response)
            else:
                await message.answer('Событие для этой пары валют не произошло!')

        elif message.text == 'FROM FILE':
            currencies_dict = read_config_file(FILE_NAME)

            for currencies, curr_cond in currencies_dict.items():
                status_response = do_job(currencies, curr_cond['trigger'], curr_cond['price'])

                if status_response != 'None':
                    await message.answer(status_response)
        else:
            await message.answer('Неправильно передана пара валют!')

    async def periodic_message_sending(user_id: int, wait_for: int):
        """
        Функция, которая раз в заданое время отправляет сообщение в случае, если сработал для одной из пар,
        заданных в файле 'config.json', валют триггер
        :param user_id: идентификатор user надо получть отдельно
        :param wait_for: цикличность отправки сообщения задается в секундах
        """
        while True:

            currencies_dict = read_config_file(FILE_NAME)

            for currencies, curr_cond in currencies_dict.items():
                status_response = do_job(currencies, curr_cond['trigger'], curr_cond['price'])

                if status_response != 'None':
                    await dp.bot.send_message(user_id, status_response)

            await asyncio.sleep(wait_for)

    loop = asyncio.get_event_loop()
    loop.create_task(periodic_message_sending(USER_ID, INTERVAL))

    executor.start_polling(dp)


