from pprint import pprint
from openai import OpenAI
import os
from settings import openapi_key, prompt_past, prompt_present, prompt_future, prompt_final
from settings import test_layout


def prediction(layout: list[dict], question: str) -> None:
    """
        This function adds prediction from chatGPT into 'prediction' "layout" dict element for each card

    """

    global prompt_past, prompt_present, prompt_future, prompt_final
    messages = []

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", openapi_key))

    for num, card in enumerate(layout):
        match num:
            case 0:
                prompt_past = prompt_past.replace("$CARD", card['name']).replace("$ASK", question)
                card['prediction'] = openai_handler(client=client, messages=messages, prompt=prompt_past)

            case 1:
                prompt_present = prompt_present.replace("$CARD", card['name'])
                card['prediction'] = openai_handler(client=client, messages=messages, prompt=prompt_present)

            case 2:
                prompt_future = prompt_future.replace("$CARD", card['name'])
                card['prediction'] = openai_handler(client=client, messages=messages, prompt=prompt_future)


    layout[0]['final_prediction'] = openai_handler(client=client, messages=messages, prompt=prompt_final)

    pprint(layout)


def openai_handler(client: OpenAI, messages: list[dict], prompt: str) -> str:

    messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=messages)
    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})

    return chat_response

# prediction(layout=test_layout, question="Закончу ли я сегодня работать с радостью на душе?")