# PART 1:
print("-"*21)
print("Exercise 1:")
print()
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
        self._balance = 0

    def deposit(self, amout):
        if amout > 0:
            self._balance += amout
            print(f"Deposited: {amout}$. New balance: {self._balance}$")
        else:
            print(f"You don't have enough fundsto deposit that amount.You only have {self._balance}$")

    def withdraw(self, amout):
        if amout <= self._balance:
            self._balance -= amout
            print(f"Withdrew: {amout}$. New balance: {self._balance}$")
        else:
            print(f"You don't have enough funds to withdraw that amount.You only have {self._balance}$")

    def get_balance(self):
        return self._balance

    def transfer(self, other_account, amout):
        if amout <= self._balance:
            self.withdraw(amout)
            other_account.deposit(amout)
            print(
                f"Transferred: {amout}$ to other account. New balance: {self._balance}$")
        else:
            print(f"You don't have enough funds to transfer that amount. You only have {self._balance}$ left.")


account1 = BankAccount() #main account for the user
account2 = BankAccount() #needed for the transfer acction

while True: #to keep the programm going till the user is finished
    action = input(
        "What would you like to do? (deposit, withdraw, transfer, balance, exit): ")
    if action == "exit":
        break
    elif action == "deposit":
        amount = float(input("Enter amount to deposit: "))
        account1.deposit(amount)
    elif action == "withdraw":
        amount = float(input("Enter amount to withdraw: "))
        account1.withdraw(amount)
    elif action == "transfer":
        amount = float(input("Enter amout to Tranfer:"))
        account1.transfer(account2, amount)
        print(f"Account 2 new balance: {account2.get_balance()}")
    elif action == "balance":
        print(f"Account 1 Current balance: {account1.get_balance()}")
        print(f"Account 2 Current balance: {account2.get_balance()}")
    else:
        print("Invalid action.")


# PART 2:
print()
print("-"*21)
print("Exercise 2:")
print()
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class French_Deck:
    def __init__ (self):
        Variants = ["Diamonds", "Hearts", "Spades", "Clubs"]
        Numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.cards = []
        for variant in Variants:
            for number in Numbers:
                self.cards.append(f"{number} of {variant}")
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, deck):
        y = 0
        while y <= 3: #its set to 3 answers for easier testing, normal case would be y == 0
            x = input("Please enter a number (0-55) or the suite name(Diamonds, Hearts, Spades, Clubs): ")
            if x.isdigit():
                x = int(x)
                if 0 <= x and x <= 56:
                    print(deck[x])
                    y += 1
                else:
                    print("Invalid Input. Please enter a Number between 0 and 55!")    
            elif x == "Diamonds":
                print(deck[0:14])
                y += 1
            elif x == "Hearts":
                print(deck[14:28])
                y += 1
            elif x == "Spades":
                print(deck[28:42])
                y += 1
            elif x == "Clubs":
                print(deck[42:56])
                y += 1
            else:
                print("Invalid Input. Please enter a number or the suite name with the first letter capitalized.")
        return deck



#Testing the French_Deck class
#print (French_Deck().cards)

#Testing the __getitem__
French_Deck.__getitem__(self=French_Deck(), deck=French_Deck().cards)


    

# PART 3:
print()
print("-"*21)
print("Exercise 3:")
print()
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class skart_deck():
    def __init__ (self):
        Suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
        Number = ["7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.cards = []
        for variant in Suits:
            for number in Number:
                self.cards.append(f"{number} of {variant}")
    def __getitem__ (self, deck):
        y = 0
        while y <= 3: #its set to 3 answers for easier testing, normal case would be y == 0
            x = input("Please enter a number (0-32) or the suite name (Diamonds, Hearts, Spades, Clubs): ")
            if x.isdigit():
                x = int(x)
                if 0 <= x and x <= 33:
                    print(deck[x])
                    y += 1
                else:
                    print("Invalid Input. Please enter a Number between 0 and 32!")    
            elif x == "Diamonds":
                print(deck[0:8])
                y += 1
            elif x == "Hearts":
                print(deck[8:16])
                y += 1
            elif x == "Spades":
                print(deck[16:24])
                y += 1
            elif x == "Clubs":
                print(deck[24:33])
                y += 1
            else:
                print("Invalid Input. Please enter a number or the suite name with the first letter capitalized.")
        return deck        

#Testing skart deck
skart_deck.__getitem__(self = skart_deck, deck = skart_deck().cards)


#Testing both decks length
assert len(French_Deck().cards) == 56, "French Deck should have 56 cards"
assert len(skart_deck().cards) == 32, "Skart Deck should have 32 cards"

#Testing indexing in both decks
assert French_Deck().cards[0] == "1 of Diamonds", "First card in French Deck should be 1 of Diamonds"
assert skart_deck().cards[0] == "7 of Diamonds", "First card in Skart Deck should be 7 of Diamonds"

#assert commands above are not silent, cause they throw no error, as proof of my working code.

#Throwing an error with assert
#assert French_Deck().cards[3] == "2 of Diamonds", "Fourth card in French Deck should be 5 of Diamonds" #Error Works
#assert skart_deck().cards[6] == "Ace of Spades", "Seventh card in Skart Deck should be Ace of Diamonds" # Error Works


# PART 4:
print()
print("-"*21)
print("Exercise 4:")
print()
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right
#

class valid_numbers():
    def __init__ (self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    def validate(self):
        valid_passwords = []
        for number in range(self.lower_bound, self.upper_bound):
            number_str = str(number)
            two = False
            for i in range(len(number_str) - 1):
                if number_str[i] == number_str[i + 1]:
                    if (i == 0 or number_str[i] != number_str[i - 1]) and (i + 1 == len(number_str) - 1 or number_str[i] != number_str[i + 2]):
                        two = True
            increasing = all(number_str[i] <= number_str[i + 1] for i in range(len(number_str) - 1))
            if two and increasing:
                valid_passwords.append(number)
        return valid_passwords




#lower_bound = 13456471
#upper_bound = 58515929
#result = valid_numbers(lower_bound, upper_bound).validate()
#print(f"Valid Results overall count: {len(result)}")
#print(f"Count of valid numbers: {result}")


print() # formating
# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `13456471` and the upper bound `58515929`.
# It should complete in a few seconds. Note the resulting count in your pull request, please.

# Valid Results overall count: 5234 [13456677:57889999]