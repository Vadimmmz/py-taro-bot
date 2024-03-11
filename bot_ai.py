from datetime import time
from pprint import pprint

import telebot
from telebot import types
from card_tools import make_layout
from chatgpt import prediction
from settings import bot_message_hello

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = '6018545480:AAEX2xkOK2ZFVt-nH5s0qJbua1QYFIlCuDY'

# Создание объекта бота
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


# Добавление нового сеанса
def add_session(user_id):
    sessions[user_id]: list[dict] = make_layout()

    prediction(layout=sessions[user_id], question="Закончу ли я сегодня работать с радостью на душе?")
    # get_prediction(sessions[user_id], question="Как долго мне ждать когда мне привезут еду с магазина?")
    # pprint(sessions[user_id])


# Получение информации о сеансе
def get_session(user_id):
    return sessions.get(user_id, None)


# Удаление сеанса
def delete_session(user_id):
    if user_id in sessions.keys():
        del sessions[user_id]


def send_start_message(chat_id, user_id, name: str):
    with open("images/cat.png", 'rb') as f:
        photo = f.read()

    # TODO put reply markup right into this func parametres
    msg = bot.send_photo(chat_id, photo, caption=bot_message_hello.replace("name", name))

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
        # msg = bot.send_message(chat_id, card['description'])

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

        bot.send_message(chat_id, card_list[0].get('final_prediction', 'Введите /start'))
        delete_session(user_id)
        if card_list[0].get('final_prediction', False):
            del card_list[0]['final_prediction']


@bot.message_handler(content_types=["text"])
def get_answer(message):
    if sessions.get(message.from_user.id):
        ...
    else:
        bot.send_message(message.chat.id, "Набери /start для начала гадания! (Добавить кнопку)")



# Обработчик нажатия на кнопку "Далее"
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data:
        if call.data.startswith("start"):
            bot.send_message(call.message.chat.id, 'Отлично! Напишите на что будем гадать?')
            call_data = call.data.split(" ")
            add_session(call_data[1])
            print(f"{get_session(call_data[1])}")

            send_cards(chat_id=call_data[2], card_list=get_session(call_data[1]),
                       index=0, user_id=call_data[1])
        else:
            call_data = call.data.split(" ")
            print(call.data)

            if get_session(call_data[1]):
                send_cards(call.message.chat.id, get_session(call_data[1]), int(call_data[0]) + 1,
                           user_id=call_data[1])
                bot.answer_callback_query(call.id)
            else:
                bot.send_message(call.message.chat.id, 'Введите чтобы начать гадать! /start')


# Запуск бота
bot.polling()
