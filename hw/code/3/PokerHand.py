"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import *
from itertools import groupby
from operator import itemgetter


class PokerHand(Hand):

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        self.ranks = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
            if card.rank == 1:
                self.ranks[card.rank + 13] = self.ranks.get(card.rank, 0) + 1
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    # Added methods

    def has_pair(self):
        self.suit_hist()
        for val in self.ranks.values():
            if val == 2:
                return True
        return False

    def has_twopair(self):
        self.suit_hist()
        count = 0
        for val in self.ranks.values():
            if val == 2:
                if count == 1:
                    return True
                count += 1
        return False

    def has_three_kind(self):
        self.suit_hist()
        for val in self.ranks.values():
            if val == 3:
                return True
        return False

    def has_straight(self):
        self.suit_hist()
        for key, group in groupby(enumerate(self.ranks.keys()), lambda (index, item): index - item):
            group = map(itemgetter(1), group)
            if len(group) > 4:
                return True
        return False

    def has_four_kind(self):
        self.suit_hist()
        for val in self.ranks.values():
            if val == 4:
                return True
        return False

    def has_straight_flush(self):
        if self.has_flush():
            if self.has_straight():
                return True
        return False

    def has_full_house(self):
        return self.has_three_kind() and self.has_pair()

    def classify(self):
        if self.has_straight_flush():
            return "Straight Flush"

        if self.has_four_kind():
            return "Four Of A Kind"

        if self.has_full_house():
            return "Full House"

        if self.has_flush():
            return "Flush"

        if self.has_straight():
            return "Straight"

        if self.has_three_kind():
            return "Three Of A Kind"

        if self.has_twopair():
            return "Two Pair"

        if self.has_pair():
            return "Pair"

if __name__ == '__main__':
    count_outcomes = {}

    for j in range(10000):
        # deal the cards and classify the hands
        deck = Deck()
        deck.shuffle()
        for i in range(7):
            hand = PokerHand()
            deck.move_cards(hand, 7)
            hand.sort()
            outcome = hand.classify()
            count_outcomes[outcome] = count_outcomes.get(outcome, 0) + 1

    print("%-20s | %-20s" % ("Hand", "Probability"))
    for i in count_outcomes.keys():
        print("%-20s | %f " % (i, count_outcomes[i]/float(70000)))
