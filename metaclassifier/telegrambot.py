"""
This is MetaClassifier.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types, exceptions, filters
import logging
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
import threading
import time
from datetime import datetime, timedelta, timezone
from typing import List
import json
import os
import pytz
from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.utils.callback_data import CallbackData
from .misc import config, swapper
os.makedirs('data', exist_ok=True)

logging.basicConfig(level=logging.INFO)
configs = config['engine']['telegram']
print(configs)

API_TOKEN = configs['apitoken']

# Configure logging
logging.basicConfig(level=logging.INFO)

loop = asyncio.new_event_loop()

# Initialize bot and dispatcher

bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop)
dp.middleware.setup(LoggingMiddleware())

# optionCallback = CallbackData('location', 'msgid', 'bus', 'direction')

startMessage = """
Bienvenido al Clasificador

Como ves aqui vamos a clasificar datos para entrenar modelos de ML

commands:

/next
"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, startMessage)


helpMessage = """
Este bot ayuda a clasificar datos para entrenar modelos de machine learning

commands:

/next
"""


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.chat.id, helpMessage)

def newquestion():
    try:
        m = swapper.get_sample()
        text, markup = format_post(m.text, m.id)

    except IndexError:
        text = 'No hay más noticias que clasificar'
        markup = types.InlineKeyboardMarkup()

    return text, markup

@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    text, markup = newquestion()

    await bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='html')


# CallBack
optionCallback = CallbackData('location','hash', 'option')


def format_post(msg: str, id: str) -> (str, types.InlineKeyboardMarkup):
    text = f"{md.hbold(msg)}\n"

    markup = types.InlineKeyboardMarkup()

    for option in swapper.options:
        markup.add(
            types.InlineKeyboardButton(option,
                                       callback_data=optionCallback.new(
                                           hash=id, option=option)), )
    return text, markup


# async def location_msg(message: types.Message):
#     text, markup = format_post(message.message_id)

#     await message.reply(text, reply_markup=markup, parse_mode='html')


# confirmation_cb = CallbackData('confirmation', 'action', 'msgid', 'bus',
#                                'direction')


def confirm_msg(msgid, bus, direction):
    d = getattr(getattr(gProvider, bus), direction).name
    msg = f"Voy en #{bus} en dirección a {d}"
    text = f"{md.hbold('Seguro que quiere enviar el mensaje:')}\n" + msg
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('👍',
                                   callback_data=confirmation_cb.new(
                                       msgid=msgid,
                                       action='accept',
                                       bus=bus,
                                       direction=direction)),
        types.InlineKeyboardButton('👎',
                                   callback_data=confirmation_cb.new(
                                       msgid=msgid,
                                       action='deny',
                                       bus=bus,
                                       direction=direction)),
    )

    return text, markup


@dp.callback_query_handler(optionCallback.filter())
async def confirmationCB(query: types.CallbackQuery):
    prefix, hash, option = query.data.split(':')
    ans = swapper.samples[hash].save(option)
    text, markup = newquestion()
    await query.message.edit_text(text, reply_markup=markup)

def run():
    # loop.create_task()
    executor.start_polling(dp, loop=loop, skip_updates=True)