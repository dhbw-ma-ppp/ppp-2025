# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.
print("Part 1:\n")
class BankAccount():

    def __init__(self, balance):
        self._balance = balance
        self.other_account = 0
        pass

    def deposit(self, ammount):
        self._balance += ammount
        print(f"You succesfully deposited {ammount}€ to your account")
        print(f"Your new balance is {self._balance}€\n")

    def withdraw(self, ammount):
        if (self._balance - ammount) > 0:
            self._balance -= ammount
            print(f"You succesfully withrew {ammount}€ from your account")
            print(f"Your new balance is {self._balance}€\n")
        else:
            print("This ammount can't be withdrawn, because your balance is to low!")

    def get_balance(self):
        print(f"Your balance is {self._balance}€\n")
    
    def transfer(self, ammount):
        if (self._balance - ammount) > 0:
            self._balance -= ammount
            self.other_account += ammount
            print(f"You succesfully transfered {ammount}€, your new balance is: {self._balance}€\n")
        else:
            print("This ammount can't be transfered, because your balance is to low!")
            print("You either have to lower the ammount or deposit money to your account.\n")

my_balance = BankAccount(50)
my_balance.deposit(100)
my_balance.withdraw(100)
my_balance.get_balance()
my_balance.transfer(200)

# PART 2:
#   Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order 
#   (2-Ace of each suite, suites in the order above)
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.
print("Part 2:\n")

class Cards:
    values = ["1","2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"] 
    suits = ["Diamonds","Hearts","Spades","Clubs"]

    def __init__(self, value, suit):
        self._value = value
        self._suit = suit

    def __str__(self):
        return f"{self._value} {self._suit}"
    
       
class FrenchDeck(Cards):
    def __init__(self,):
        self._deck = [Cards(s, v) for s in Cards.suits for v in Cards.values] 
        pass

    def __str__(self):
        return "\n".join([str(Karte) for Karte in self._deck]) 
      
    def __getitem__(self, index):
        return (self._deck[index])  


# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck(Cards):
    def __init__(self,):
        self._deck = [Cards(s, v) for s in Cards.suits for v in Cards.values[6:]]
        pass

    def __str__(self):
        return "\n".join([str(Karte) for Karte in self._deck])
      
    def __getitem__(self, index):
        return (self._deck[index])
    
my_skat_deck = SkatDeck()
my_french_deck = FrenchDeck()
my_card = Cards("King","Spade")
print("I should be able to iterate over all cards in the deck.\n")
print("Frenchdeck:\n")
for i in my_french_deck:
    print(i)
print("\nSkatdeck:\n")
for i in my_skat_deck:
    print(i)
print(f"\nI should be able to index into the deck to retrieve one card.\n\nFrenchdeck:\n{my_french_deck[4]}\n\nSkatdeck:\n{my_skat_deck[4]}\n")
print(f"Printing a cards string representation should give me a nice, readable description of that card.:\n{my_card}")



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

print("\nPart 4\n")

def zerleger(lower_bound, upper_bound):
    list_numbers_criteria1_2 = []
    list_numbers_criteria1_2_3 = []

    #one group of exactly two adjacent digits wich are the same

    for zahl in range(lower_bound, upper_bound):
        zahl = str(zahl)
        x = 0
        for index in range(len(zahl)):
            if index == 0:
                if zahl[index] == zahl[index + 1] and zahl[index] != zahl[index + 2]: 
                    x += 1
            elif 0 < index < len(zahl) - 2:
                if zahl[index] == zahl[index + 1] and zahl[index] != zahl[index + 2] and zahl[index] != zahl[index - 1]: 
                    x += 1
            elif index == len(zahl) - 2:
                if zahl[index] == zahl[index + 1] and zahl[index] != zahl[index - 1]:                    
                    x += 1 
            elif index == len(zahl) - 1:
                if x >= 1:
                    list_numbers_criteria1_2.append(zahl)

    #check if all digits are relativly to the digit in front of them increasing
    for zahl in list_numbers_criteria1_2:
        zahl = str(zahl)
        for index in range(len(zahl)):
            if index < len(zahl) - 1: 
                if zahl[index] > zahl[index + 1]:
                    break
                if index == len(zahl) -2:
                    list_numbers_criteria1_2_3.append(zahl)
                    break
                if zahl[index] < zahl[index + 1]:
                    continue              
           
    
    count_numbers = len(list_numbers_criteria1_2_3)
    return count_numbers      
print(f"Count of numbers that meet all criterias: {zerleger(13456471,58515929)}")