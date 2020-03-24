#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with aiohttp
# It echoes any incoming text messages and does not use the polling method.

from datetime import datetime
import logging
import ssl

from aiohttp import web
from credentials.tokens import TOKEN, HOST_IP
from google.cloud import bigquery
import telebot

from main_logic.common_const.common_const import USERS_COLLECTION
from main_logic.google_cloud.clients import DatastoreClient
from main_logic.image_processing import image_crop
from main_logic.state_handling.quest_states import QuestState, QuestStateType
from main_logic.state_handling.state_handler import get_user_state
from main_logic.user_managment.users_crud import User

API_TOKEN = TOKEN

WEBHOOK_HOST = HOST_IP
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = 'credentials/url_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'credentials/url_private.key'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = web.Application()


# Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post('/{token}/', handle)

client = bigquery.Client()


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def init_state(message):
    telegram_id = message.from_user.id

    user = User.get_user_by_telegram_id(telegram_id=telegram_id)
    if not user:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        user = User(
            user_id='',
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
        )
        user.add_to_db()
    print(f'us: {user}')
    state_type = None
    if user:
        state = get_user_state(user=user)
        if state:
            state_type = state.state_type

    if not state_type:
        state_type = QuestStateType.MODE_SELECTION

    state_handler = QuestState(current_state=state_type)
    available_actions = state_handler.get_triggers()
    bot.reply_to(message, f'{available_actions}')


@bot.message_handler(commands=['new'])
def send_welcome(message):
    # user_id = message.from.user_id
    # print(message, message.from_user)

    user_id = message.from_user.id
    QUERY = f'SELECT * FROM `users_BFemKh4v.users_info` WHERE user_id="{user_id}"'
    res = client.query(query=QUERY)
    res = list(res)

    assert len(res) < 2
    finded = len(res) == 1
    if not finded:
        ts = int(message.date)
        reg_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        QUERY_INSERT = f'INSERT `users_BFemKh4v.users_info` (user_id, user_name, registration_date) VALUES ("{message.from_user.id}", "{message.from_user.username}", "{reg_date}")'
        print(f'query={QUERY_INSERT}')
        status = client.query(query=QUERY_INSERT)
        print(f'inserted: {res}')
        user_name = message.from_user.username
    else:
        user_name = res[0][1]
        status = 'OK'
    bot.reply_to(message,
                 (f"Hi {user_name}! I am EchoBot.\n"
                  f"I am here to echo your kind words back to you. "
                  f"Your id = {message.from_user.id} status={status}"))

# Handle image uploads
@bot.message_handler(func=lambda message: True, content_types=['photo'])
def upload_photo(message):
    chat_id = message.chat.id
    for photo in message.photo:
        photo_id = photo.file_id
        bot.reply_to(message, 'get photo with metadata: ' + str(photo_id))
        # process_file

        name = photo_id + ".jpg"
        file_info = bot.get_file(photo_id)
        print(f'finfo: {file_info}')
        downloaded_file = bot.download_file(file_info.file_path)

        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)

        all_images = image_crop.crop_images(file_name=name)
        img = open(all_images[1], 'rb')
        bot.send_message(chat_id, "Запрос от\n*{name} {last}*".format(
            name=message.chat.first_name, last=message.chat.last_name),
                         parse_mode="Markdown")  # от кого идет сообщение и его содержание
        bot.send_photo(chat_id, img)
        # end proceess
    # bot.send_photo(message.chat.id, photo_id)

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)

