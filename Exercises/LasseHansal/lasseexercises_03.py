# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.S

class BankAccount:
    def __init__(self, _balance):
        self._balance = _balance

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Error: Deposit amount must be positive")
        
        self._balance += amount
        print(self.get_balance())
    
    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Error: Withdraw amount must be positive")
        if self._balance < amount:
            print("Error: Withdraw failed due to insufficient funds")
            return False
        self._balance -= amount
        print(self.get_balance())
        return True

    def transfer(self, other_account, amount):
        if amount < 0:
            raise ValueError("Error: Transfer amount must be positive")

        if self.withdraw(amount):
            other_account.deposit(amount)
            print("Transfer successful")
        else:
            print("Error: Transfer failed due to insufficient funds")

        print(f"Account (source)        Balance: {self.get_balance()}")
        print(f"Account (destination)   Balance: {other_account.get_balance()}")
    

if __name__ == "__main__":
    print("Task 1:\n")

    account = BankAccount(100)
    account2 = BankAccount(100)

    print("Initial Balances:")
    print(f"Account 1: {account.get_balance()}")
    print(f"Account 2: {account2.get_balance()}")

    print("\nDepositing: (Account 1) +50")
    account.deposit(50)

    print("\nWithdrawing: (Account 1) -50")
    account.withdraw(50)

    print("\nTransferring: (Account 1 -> Account 2) 50")
    account.transfer(account2, 50)

    print("\nAttempting an invalid transfer (Account 1 -> Account 2) 1000:")
    account.transfer(account2, 1000)


# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    
    def __repr__(self):
        return f"{self.suit} : {self.number}"

class Deck:

    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self._cards = []

        for suit in self.suits:
            for number in self.numbers:
                self._cards.append(Card(suit, number))
    
    def __getitem__(self, input):
        return self._cards[input]


if __name__ == "__main__":
    print("\nTask 2:\n")

    french_deck = Deck()

    print("String Test:")
    first_card = french_deck[0]
    mid_card = french_deck[15]
    last_card = french_deck[-1]
    
    print(f"First Card: {first_card}")
    print(f"Mid Card: {mid_card}")
    print(f"Last Card: {last_card}")

    print("\nIndex Test:")
    print(f"Card at index 3: {french_deck[3]}")
    
    print("\nLoop Test:")
    for card in french_deck:
        print(card)

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
class SkatDeck:
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    numbers = [7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self._cards = []

        for suit in self.suits:
            for number in self.numbers:
                self._cards.append(Card(suit, number))
    
    def __getitem__(self, input):
        return self._cards[input]
    
    def __len__(self):
        return len(self._cards)

if __name__ == "__main__":
    print("\nTask 3:\n")

    skat_Deck = SkatDeck()

    print("String Test:")
    first_card = skat_Deck[0]
    mid_card = skat_Deck[skat_Deck.__len__() // 2]
    last_card = skat_Deck[-1]
    
    print(f"First Card: {first_card}")
    print(f"Mid Card: {mid_card}")
    print(f"Last Card: {last_card}")

    print("\nIndex Test:")
    print(f"Card at index 3: {skat_Deck[3]}")
    
    print("\nLoop Test:")
    for card in skat_Deck:
        print(card)

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
def check_numbers(lower_bound: int, upper_bound: int) -> int:
    count = 0
    
    for number in range(lower_bound, upper_bound):
        digits = []
        n = number
        while n > 0:
            digits.append(n % 10)
            n //= 10
        digits.reverse()

        is_increasing = True
        for i in range(len(digits) - 1):
            if digits[i] > digits[i + 1]:
                is_increasing = False
                break
        
        if not is_increasing:
            continue
        
        has_exact_pair = False
        i = 0
        while i < len(digits):
            j = i
            while j < len(digits) and digits[j] == digits[i]:
                j += 1
            
            if j - i == 2:
                has_exact_pair = True
                break
            
            i = j
        
        if has_exact_pair:
            count += 1
    
    return count

result = check_numbers(13456471, 58515929)
print(f"Count of valid numbers: {result}")