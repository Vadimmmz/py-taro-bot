from pprint import pprint

from card_deck import card_deck
import random


def make_layout() -> list[dict]:
    layout = []

    while len(layout) < 3:
        card = random.choice(card_deck)

        names = [x['name'] for x in layout] if layout else []
        if card['name'] not in names:
            layout.append(card)

    # TODO del this part
    cards_names = [x['name'] for x in layout]
    print(cards_names)
    # for here

    return layout

# def get_random_card():
#     card = random.choice(card_deck)
#     return card

# def get_card_from_layout(layout: list) -> list[list]:
#     return layout.pop(0)
#
#
# def get_layout() -> list[dict]:
#
#     result = []
#     x = make_layout()
#     while x:
#         result.append(get_card_from_layout(x))
#
#     return result

# def final_layout() -> dict[dict]:
#
#     result = dict()
#     x = make_layout()
#     while x:
#         match len(x):
#             case 3:
#                 result['past'] = get_card_from_layout(x)
#             case 2:
#                 result['present'] = get_card_from_layout(x)
#             case 1:
#                 result['future'] = get_card_from_layout(x)
#
#     return result


# pprint(final_layout())