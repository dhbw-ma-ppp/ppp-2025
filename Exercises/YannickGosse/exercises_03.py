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
    def __init__(self, account_number):
        self.account_number = account_number
        self._balance = 0

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        self._balance -= amount

    def get_balance(self):
        return self._balance
    
    def transfer(self, other_account, amount):
        other_account.deposit(amount)
        self.withdraw(amount)

def select_action(account):
    while True:
        print("\n1. deposit \n2. withdraw \n3. show balance \n4. transfer money \n5. exit (Use to see other tasks)")
        try:
            action = int(input("To select an option input it's number: "))
        except ValueError:
            print("Please input a valid number.")
            continue
        if action == 5:
            print("Goodbye!\n")
            break
        elif action == 1:
            try:
                a = float(input("How much money do you want to deposit? "))
                account.deposit(a)
                print(f"Deposited {a}. New balance is: {account.get_balance()}")
            except ValueError:
                print("Invalid amount.")
        elif action == 2:
            try:
                a = float(input("How much money do you want to withdraw? "))
                if a <= account.get_balance():
                    account.withdraw(a)
                    print(f"Withdrawn {a}. New balance is: {account.get_balance()}")
                else:
                    print("Insufficient funds.")
            except ValueError:
                print("Invalid amount.")
        elif action == 3:
            print("Your current balance is: ", account.get_balance())
        elif action == 4:
            try:
                a = float(input("How much money do you want to transfer? "))
                if a <= account.get_balance():
                    other_account = BankAccount0 = BankAccount(input("Account number of the receiver: "))
                    account.transfer(other_account,a)
                    print(f"Transferd {a}.  Your new balance is: {account.get_balance()} \nThe other accounts balance is: {other_account.get_balance()}")
                else:
                    print("Insufficient funds.")
            except ValueError:
                print("Invalid amount.")
        else: 
            print("Please input a valid option.")

action = 0
print("Welcome!")
account_num = input("Please enter your account number: ")
BankAccount1 = BankAccount(account_num)
select_action(BankAccount1)


# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f'{self.value} of {self.suit}'
        

class FrenchDeck:
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]

    def __init__(self):
        self._deck = [Card(value, suit) for suit in self.suits for value in self.values]
    
    def get_deck(self):
        return [str(element) for element in self._deck]
    
    def __getitem__(self, position):
        return self._deck[position]

Deck1 = FrenchDeck()
print("French Deck: ", Deck1.get_deck())
print(f"\nFirst card (index = 0): {Deck1[0]}")
print(f"Last card (index = 51): {Deck1[51]} \n")
assert str(Deck1[0]) == "2 of Diamonds"
assert str(Deck1[12]) == "Ace of Diamonds"
assert str(Deck1[51]) == "Ace of Clubs"
print("Iterating the first five cards: \n")
count = 0
for card in Deck1:
    if count < 5:
        print(f"  {card}")
    count += 1


# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck(FrenchDeck):
    values = ["7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]


Deck2 = SkatDeck()
print("Skat Deck: ", Deck2.get_deck())
print(f"\nFirst card (index = 0): {Deck2[0]}")
print(f"Last card (index = 31): {Deck2[31]} \n")
assert str(Deck2[0]) == "7 of Diamonds"
assert str(Deck2[12]) == "Jack of Hearts"
assert str(Deck2[31]) == "Ace of Clubs"
print("Iterating the first five cards: \n")
count = 0
for card in Deck1:
    if count < 5:
        print(f"  {card}")
    count += 1


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


def count_valid_combinations(l_bound, u_bound):
    count = 0
    if l_bound >= u_bound:
        print("Lower bound must be smaller than upper bound.")
        return 0

    for num in range(l_bound, u_bound):
        if meets_criteria(num) == True:
            count += 1
    return count


def meets_criteria(number):
    string_n = str(number)
    n_len = len(string_n)

    for index in range(n_len - 1):
        if int(string_n[index]) > int(string_n[index + 1]):
            return False

    i = 0
    while i < n_len - 1:
        if string_n[i] == string_n[i + 1]:
            group_size = 2
            j = i + 2

            while j < n_len and string_n[j] == string_n[i]:
                group_size += 1
                j += 1

            if group_size == 2:
                return True

            i = j
        else:
            i += 1

    return False
    
lower_bound = 13456471
upper_bound = 58515929
print("The result for the example is: ", count_valid_combinations(lower_bound, upper_bound))