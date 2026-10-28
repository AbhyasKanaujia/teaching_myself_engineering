import collections
from random import choice
from typing import ClassVar

Card = collections.namedtuple("Card", ["rank", "suit"])
suit_value = {"spades": 3, "hearts": 2, "diamonds": 1, "clubs": 0}


class FrenchDeck:
    ranks: ClassVar[list[str]] = [str(n) for n in range(2, 11)] + list("JQKA")
    suites: ClassVar[list[str]] = ["spades", "diamonds", "clubs", "hearts"]

    def __init__(self):
        self._cards = [
            Card(rank, suite) for suite in self.suites for rank in self.ranks
        ]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


beer_card = Card("7", "diamonds")
print(repr(beer_card))
deck = FrenchDeck()
print(len(deck))
print(deck[0])
print(deck[-1])
print(choice(deck))
print("Top 3 cards:", deck[:3])
print("Aces only:", deck[12::13])

print("First 5:")
for card in deck[0:5]:
    print(card)
print("Last 5:")
for card in deck[::-1][0:5]:
    print(card)

print(Card("7", "hearts") in deck)
print(Card("7", "beats") in deck)
