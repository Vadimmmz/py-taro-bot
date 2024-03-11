from datetime import time
from pprint import pprint

import telebot
from telebot import types
from card_tools import make_layout
from chatgpt import prediction
from settings import bot_message_hello, bot_message_await, mock_layout, telegram_token, bot_message_askme, \
    bot_message_start

TOKEN = telegram_token
bot = telebot.TeleBot(TOKEN)

sessions = {}


class Session():
    """
        Keeps user session info required for prediction

    """

    def __init__(self, user_id, layout: list[dict]):
        self.user_id = user_id
        self.cards = layout

        self.prediction_in_process = True

        self.first_prediction = None
        self.second_prediction = None
        self.third_prediction = None
        self.final_prediction = None

    def get_card(self) -> dict:
        return self.cards.pop(0)


def add_session(user_id):
    sessions[int(user_id)]: list[dict] = make_layout()


def get_session(user_id):
    return sessions.get(int(user_id), None)


def delete_session(user_id):
    if int(user_id) in sessions.keys():
        del sessions[int(user_id)]
        print("DELETED")


def send_start_message(chat_id, user_id, name: str):
    with open("images/cat.png", 'rb') as f:
        photo = f.read()

    # TODO put reply markup right into this func parametres
    msg = bot.send_photo(chat_id, photo, caption=bot_message_hello.replace("$NAME", name))

    # Создание кнопки "Далее"
    markup = types.InlineKeyboardMarkup()
    btn_next = types.InlineKeyboardButton('Гадать', callback_data=f"start {user_id} {chat_id}")
    markup.add(btn_next)

    # Привязка кнопки к сообщению
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg.message_id, reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    send_start_message(chat_id=message.chat.id, name=message.from_user.first_name, user_id=message.from_user.id)


# Функция отправки предсказания пользователю
def send_cards(chat_id, card_list, index, user_id):
    if index < len(card_list):
        card = card_list[index]

        with open(card['image'], 'rb') as f:
            photo = f.read()

        msg = bot.send_photo(chat_id, photo, caption=card['prediction'])

        # Создание кнопки "Далее"
        markup = types.InlineKeyboardMarkup()
        btn_next = types.InlineKeyboardButton('Далее', callback_data=f"{index} {user_id}")
        markup.add(btn_next)

        # Привязка кнопки к сообщению
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg.message_id, reply_markup=markup)
    else:

        bot.send_message(chat_id, card_list[0].get('final_prediction'))
        bot.send_message(chat_id, bot_message_start)
        delete_session(user_id)
        if card_list[0].get('final_prediction', False):
            del card_list[0]['final_prediction']


@bot.message_handler(content_types=["text"])
def get_answer(message):
    if sessions.get(message.from_user.id):
        print(message.text)

        bot.send_message(message.chat.id, bot_message_await.replace("$NAME", message.from_user.first_name))

        # prediction(layout=sessions[message.from_user.id], question=message.text)
        # Mock
        sessions[message.from_user.id] = mock_layout

        send_cards(chat_id=message.chat.id, card_list=get_session(message.from_user.id),
               index=0, user_id=message.from_user.id)

    else:
        bot.send_message(message.chat.id, bot_message_start)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data:
        if call.data.startswith("start"):
            bot.send_message(call.message.chat.id, bot_message_askme)
            call_data = call.data.split(" ")
            add_session(int(call_data[1]))
            print(f"{get_session(int(call_data[1]))}")

        else:
            call_data = call.data.split(" ")
            print(call.data)

            if get_session(call_data[1]):
                send_cards(call.message.chat.id, get_session(call_data[1]), int(call_data[0]) + 1,
                           user_id=call_data[1])
                bot.answer_callback_query(call.id)
            else:
                bot.send_message(call.message.chat.id, bot_message_start)

# run bot
bot.polling()
