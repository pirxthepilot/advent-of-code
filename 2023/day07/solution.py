from __future__ import annotations

import json
import sys
from typing import List


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Hand:
    card_map = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.counts = self._get_card_counts()
        self.type = self._get_type()
        self.bid = bid

    def __repr__(self) -> str:
        return f"Cards: {self.cards} | Type: {self.type} | Bid: {self.bid} | {self.counts}"
    
    def _get_card_counts(self) -> List[int]:
        counts = []
        for d in set(self.cards):
            counts.append(len([i for i in self.cards if i == d]))
        return counts
    
    def _get_type(self) -> int:
        # 7: Five of a kind
        if 5 in self.counts:
            return 7

        # 6: Four of a kind
        if 4 in self.counts:
            return 6

        # 5: Full house
        if (
            3 in self.counts and
            2 in self.counts
        ):
            return 5

        # 4: Three of a kind
        if 3 in self.counts:
            return 4

        # 3: Two pair
        if len([c for c in self.counts if c == 2]) == 2:
            return 3
    
        # 2: One pair
        if len([c for c in self.counts if c == 2]) == 1:
            return 2
    
        # 1: High card
        if len(set(self.cards)) == 5:
            return 1

    def _card_value(self, card: str) -> int:
        return self.card_map[card] if card.isalpha() else int(card)
    
    def __eq__(self, other: Hand):
        return self.cards == other.cards

    def __gt__(self, other: Hand):
        if self.type == other.type:
            for i in range(len(self.cards)):
                if self._card_value(self.cards[i]) == self._card_value(other.cards[i]):
                    continue
                return self._card_value(self.cards[i]) > self._card_value(other.cards[i])
        return self.type > other.type

    def __lt__(self, other: Hand):
        if self.type == other.type:
            for i in range(len(self.cards)):
                if self._card_value(self.cards[i]) == self._card_value(other.cards[i]):
                    continue
                return self._card_value(self.cards[i]) < self._card_value(other.cards[i])
        return self.type < other.type


class Hands:
    def __init__(self, text: str):
        self.hands = []

        for line in text:
            hand, bid = line.split(" ")
            self.hands.append(Hand(hand, int(bid)))
    
    def __iter__(self):
        return iter(self.hands)

    def __repr__(self):
        return json.dumps([str(h) for h in self.hands], indent=4)
    
    def winnings(self) -> int:
        self.hands.sort()
        amount = 0
        for idx, hand in enumerate(self.hands):
            rank = idx + 1
            amount += hand.bid * rank
        return amount


def s1(hands: Hands) -> int:
    return hands.winnings()


hands = Hands(text)
print(s1(hands))
