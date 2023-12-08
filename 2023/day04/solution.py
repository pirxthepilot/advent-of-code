import re
import sys
from collections import defaultdict
from typing import List, Set


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Card:
    def __init__(self, line: str):
        m = re.match(
            r"Card\s+(?P<card_id>\d+):\s+(?P<wins>(\d+\s+)+)\|\s+(?P<have>.+)$",
            line
        )
        self.id = int(m["card_id"])
        self.winning = self._nums_from_string(m["wins"])
        self.have = self._nums_from_string(m["have"])

    @staticmethod
    def _nums_from_string(string: str) -> Set[int]:
        items = string.split(" ")
        return set([int(i.strip()) for i in items if i])

    def get_matches(self) -> Set[int]:
        return self.winning.intersection(self.have)
 
    @property
    def value(self) -> int:
        match_length = len(self.get_matches())
        return pow(2, match_length - 1) if match_length else 0


def s1(cards: List[Card]) -> int:
    return sum([card.value for card in cards])


def s2(cards: List[Card]) -> int:
    """
    Data structure
    {
        card_id: count,
        (..)
    }
    """
    inventory = defaultdict(int)

    for card in cards:
        matches = len(card.get_matches())

        # Original
        inventory[card.id] += 1

        # Copies
        for copy_card_id in range(card.id + 1, card.id + 1 + matches):
            if copy_card_id <= len(cards):
                inventory[copy_card_id] += inventory[card.id]
    
    return sum([i for i in inventory.values()])


cards = [Card(line) for line in text]
print(s1(cards))
print(s2(cards))
