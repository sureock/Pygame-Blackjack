import random


class deck52:
    def __init__(self):
        self.cards = [x for x in range(56)]
        self.cards_left = 56

    def draw(self):
        if self.cards_left == 0:
            return 'There is no card to pick'

        card = 'N'
        while card == 'N':
            if self.cards_left == 0:
                return 'Deck is empty'

            card = random.choice(self.cards)
            suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
            values = [('1', 1),
                      ('2', 2),
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

        return suits[card // 14], values[card % 14]

    def shuffle(self):
        self.cards = [x for x in range(56)]
        self.cards_left = 56
