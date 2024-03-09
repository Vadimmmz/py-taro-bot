from pprint import pprint

import telebot
from telebot import types
from card_tools import make_layout
from chatgpt import get_prediction

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = '6018545480:AAEX2xkOK2ZFVt-nH5s0qJbua1QYFIlCuDY'

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

sessions = {}


# Добавление нового сеанса
def add_session(user_id):
    sessions[user_id]: list[dict] = make_layout()
    get_prediction(sessions[user_id], question=" ли мне пить чай тем как закончить написание программы?")
    pprint(sessions[user_id])


# Получение информации о сеансе
def get_session(user_id):
    return sessions.get(user_id)


# Удаление сеанса
def delete_session(user_id):
    if user_id in sessions:
        del sessions[user_id]


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    add_session(message.from_user.id)
    send_word(message.chat.id, get_session(message.from_user.id), 0, message.from_user.id)


# Функция отправки предсказания пользователю
def send_word(chat_id, card_list, index, user_id):
    if index < len(card_list):
        card = card_list[index]
        # msg = bot.send_message(chat_id, card['description'])

        with open(card['image'], 'rb') as f:
            photo = f.read()

        msg = bot.send_photo(chat_id, photo, caption=card['description'])

        # Создание кнопки "Далее"
        markup = types.InlineKeyboardMarkup()
        btn_next = types.InlineKeyboardButton('Далее', callback_data=f"{index} {user_id}")
        markup.add(btn_next)

        # Привязка кнопки к сообщению
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg.message_id, reply_markup=markup)
    else:
        delete_session(user_id)
        bot.send_message(chat_id, card_list[0].get('final_prediction', 'Введите /start'))

        if card_list[0].get('final_prediction', False):
            del card_list[0]['final_prediction']


# Обработчик нажатия на кнопку "Далее"
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data:
        call_data = call.data.split(" ")
        print(call.data)
        send_word(call.message.chat.id, get_session(int(call_data[1])), int(call_data[0]) + 1, user_id=call_data[1])
        bot.answer_callback_query(call.id)


# Запуск бота
bot.polling()
