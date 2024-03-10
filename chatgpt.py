from pprint import pprint

from openai import OpenAI
import os

from settings import openapi_key, prompt


def prediction(layout=None, question=None):
    cards = ['two cups', 'straight', 'fool']

    for num, card in enumerate(cards):
        match num:
            case 0:
                print(f"first openai: {card}")
            case 1:
                print(f"second openai: {card}")
            case 2:
                print(f"third openai: {card}")

    print("final msg")


def prediction_openai_handler(cards: str, question: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", openapi_key))

    formatted_question = f"Карты: {cards}. Вопрос: {question}?"

    messages = [{"role": "system",
                 "content": prompt},
                {"role": "user", "content": formatted_question}]

    completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=messages)

    chat_response = completion.choices[0].message.content
    print(chat_response)
    print(type(chat_response))

    return chat_response


def get_prediction(layout: list[dict], question: str):
    cards = ', '.join([x['name'] for x in layout])

    prediction = prediction_openai_handler(cards, question).split("=SEP=")

    if len(prediction) > len(layout) + 1:
        for card, pred in zip(layout, prediction[1:]):
            card['description'] = pred
    else:
        for card, pred in zip(layout, prediction):
            card['description'] = pred

    # Keeping the last message from chat GPT in the first element of layout
    layout[0]['final_prediction'] = prediction[-1:]

# prediction()