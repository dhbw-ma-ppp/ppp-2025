from __future__ import (
    annotations,
)  # allows using the class itself as a type hint before it is fully defined


# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.


class BankAccount:
    def __init__(self):
        self._balance: float = 0

    @property
    def balance(self) -> float:
        return self._balance

    def get_balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def transfer(self, other_account: BankAccount, amount: float) -> bool:
        if self.withdraw(amount):
            other_account.deposit(amount)
            return True
        return False


# Testing
print("1)")

account1 = BankAccount()
account2 = BankAccount()
print(
    f"Initial account 1 balance: {account1.balance}\n"
    f"Initial account 2 balance: {account2.balance}"
)

account1.deposit(100)
print(f"After depositing 100 into Account 1: {account1.balance}")

if account1.withdraw(30):
    print(f"After withdrawing 30 from Account 1: {account1.balance}")
else:
    print("Withdrawal failed")

if account1.transfer(account2, 50):
    print(
        "After transferring 50 from Account 1 to Account 2:\n"
        f"Account 1 balance: {account1.balance}\n"
        f"Account 2 balance: {account2.balance}"
    )
else:
    print("Transfer failed")

if not account1.withdraw(100):
    print("Failed to withdraw 100 from Account 1 (insufficient funds)")

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"


class FrenchDeck:
    ranks = list(range(2, 11)) + list("JQKA")
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]

    def __init__(self):
        self._cards: list[Card] = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position: int) -> Card:
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)  # not needed here but recommended


# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class SkatDeck(FrenchDeck):
    ranks = list(range(7, 11)) + list("JQKA")


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

print("\n2+3)")

french_deck = FrenchDeck()


def test_deck_class(deck_class):
    deck = deck_class()
    class_name = deck_class.__name__
    print(f"\nTesting class {class_name}:")

    assert len(deck) > 0, f"❌ {deck_class.__name__} should have at least one card"
    assert (
        deck[0] is not None
    ), f"❌ {deck_class.__name__} first card should not be None"
    assert (
        deck[-1] is not None
    ), f"❌ {deck_class.__name__} last card should not be None"

    print(
        f"The class {class_name} has {len(deck)} cards.\n"
        f"First Card: {deck[0]}, Last Card: {deck[-1]}"
    )
    for card in deck:
        pass

    print("The class is iterable!")

    print(f"✅ All tests passed")


test_deck_class(FrenchDeck)
test_deck_class(SkatDeck)

# PART 4:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right
#
# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `13456471` and the upper bound `58515929`.
# It should complete in a few seconds. Note the resulting count in your pull request, please.
