# Use namedtuple to created class with attributes but no methods. 
# Like a single DB row. 


# Using plain tuple
from collections import namedtuple

card = ("7", "diamonds")
card[0]  # 7 <- we keep forgetting what index 0 was
card[1]  # diamonds <- same issue as using pair in C++ what is first? what is second?

# Using class helps


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


# First approach: Tuple is too value
# Second approach: Class is too verbose

# Balanced appraoch: use namedtuple

Card2 = namedtuple("Card", "rank suit")

c = Card2("7", "diamonds")  # positional
c = Card2(rank="6", suit="hearts")  # order doesn't matter

c.rank  # 7 <- by name
c.suit  # diamond
c[0]  # 7 <- by index

# Card(rank='7', suit='diamond') <- free, readable repr

rank, suit = c  # works, because its just a tuple
