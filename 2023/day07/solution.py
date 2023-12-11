from __future__ import annotations

import json
import sys
from typing import List, Tuple


FILE = "test.txt" if len(sys.argv) == 2 and sys.argv[1] == "test" else "input.txt"


with open(FILE, "r") as f:
    text = [t.strip() for t in f.readlines()]


class Hand:
    card_map = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.counts = self._get_card_counts(self.cards)
        self.type = self._get_type(self.cards)
        self.bid = bid

    def __repr__(self) -> str:
        return f"Cards: {self.cards} | Type: {self.type} | Bid: {self.bid} | {self.counts}"
    
    @staticmethod
    def _get_card_counts(cards: str) -> List[int]:
        counts = []
        for d in set(cards):
            counts.append(len([i for i in cards if i == d]))
        return counts
    
    def _get_type(self, cards: str) -> int:
        counts = self._get_card_counts(cards)

        # 7: Five of a kind
        if 5 in counts:
            return 7

        # 6: Four of a kind
        if 4 in counts:
            return 6

        # 5: Full house
        if (
            3 in counts and
            2 in counts
        ):
            return 5

        # 4: Three of a kind
        if 3 in counts:
            return 4

        # 3: Two pair
        if len([c for c in counts if c == 2]) == 2:
            return 3
    
        # 2: One pair
        if len([c for c in counts if c == 2]) == 1:
            return 2
    
        # 1: High card
        if len(set(cards)) == 5:
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


class JokeredHand(Hand):
    card_map = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.effective_cards, self.type = self._get_effective_hand_and_type()
        self.counts = self._get_card_counts(self.effective_cards)
        self.bid = bid
    
    def _get_effective_hand_and_type(self) -> Tuple[str, int]:
        """ Find the most optimal Joker config """
        if "J" not in self.cards:
            return self.cards, self._get_type(self.cards)
        
        if self.cards == "JJJJJ":
            return "AAAAA", self._get_type("AAAAA")

        best = None
        for replacement in set(self.cards):
            if replacement != "J":
                test_hand = self.cards.replace("J", replacement)
                test_type = self._get_type(test_hand)
                if (
                    best is None or
                    test_type > best[1]
                ):
                    best = test_hand, test_type
        return best


class Hands:
    def __init__(self, text: str, joker: bool = False):
        self.hands = []

        for line in text:
            hand, bid = line.split(" ")
            if joker:
                self.hands.append(JokeredHand(hand, int(bid)))
            else:
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

def s2(hands: JokeredHand) -> int:
    return hands.winnings()


print(s1(Hands(text)))
print(s2(Hands(text, joker=True)))
