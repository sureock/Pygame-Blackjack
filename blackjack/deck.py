"""Модуль колоды"""

import random


class deck52:
    """Класс deck52: колода на 52 карты"""

    def __init__(self):
        """Инициализация колоды"""

        self.base_condition = [x for x in range(52)]
        self.cards = self.base_condition
        self.cards_left = 52

    def draw(self):
        """Метод извлечения карты. Заменяет извлеченную карту на 'N'.

        Returns:
            tuple: масть (str), (достоиноство (str), значение (int)).

        Raises:
            ValueError: если колода закончилась.
        """

        if self.cards_left == 0:
            raise ValueError('Deck is empty, shuffle it')

        card = 'N'
        while card == 'N':
            card = random.choice(self.cards)
            suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
            values = [('2', 2),
                      ('3', 3),
                      ('4', 4),
                      ('5', 5),
                      ('6', 6),
                      ('7', 7),
                      ('8', 8),
                      ('9', 9),
                      ('10', 10),
                      ('Jack', 10),
                      ('Queen', 10),
                      ('King', 10),
                      ('Ace', 11)
                      ]

        self.cards[card] = 'N'
        self.cards_left = self.cards_left - 1

        return suits[card // 13], values[card % 13]

    def shuffle(self):
        "Возвращает колоду в базовое состояние"

        self.cards = self.base_condition
        self.cards_left = 52
