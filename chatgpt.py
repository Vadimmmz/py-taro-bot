from pprint import pprint

from openai import OpenAI
import os

key = "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"
key2 = "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"


def prediction_openai_handler(cards: str, question: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", key2))

    final_question = f"Карты: {cards}. Вопрос: {question}?"

    messages = [{"role": "system",
                 "content": "Ты гадалка цыганка, которая гадает по картам Таро. Твоя речь настолько циганская, насколько это возможно. Отвечаешь на русском с использованием жаргонных слов"
                            "Я говорю какие карты мне выпали и задаю вопрос. Ты говоришь мне расклад по трем картам Таро про этот вопрос."
                            " Ответ состоит из только из четырех абзацев: 1 карта - карта прошлого, 2 карта - карта настоящего, "
                            "3 карта - карта будущего, итоговое толкование расклада. Пиши названия карт на русском. Разделяй каждый абзац словом '=SEP=' "},
                {"role": "user", "content": final_question}]

    completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=messages)

    chat_response = completion.choices[0].message.content
    print(chat_response)
    print(type(chat_response))

    return chat_response


def get_prediction(layout: list[dict], question: str):
    cards = ', '.join([x['name'] for x in layout])

    prediction = prediction_openai_handler(cards, question).split("=SEP=")

    for card, pred in zip(layout, prediction[1:]):
        card['description'] = pred
        # print(prediction)

    # Keeping last message from chat GPT in first element of layout
    layout[0]['final_prediction'] = prediction[-1:]

# prediction_openai_handler()
