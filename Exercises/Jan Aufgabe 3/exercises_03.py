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
    __attribute_balance__ = 0
    def __init__(self):
        self._balance = 0

    def deposit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
        else:
            print("Nicht genug Geld auf dem Konto") 

    def get_balance(self):
        return self._balance

    def transfer(self, other_account, amount):
        if amount <= self._balance:
            self._balance -= amount
            other_account.deposit(amount)
        else:
            print("Nicht genug Geld auf dem Konto")



# Beispiel:
account1 = BankAccount()
account2 = BankAccount()

def eingabe():
    choice = input("Möchten Sie Geld einzahlen (E), abheben (A) oder überweisen (Ü)? ")
    if choice == "E":
        betrag = float(input("Betrag eingeben: "))
        account1.deposit(betrag)
        print("Konto1: Kontoguthaben nach Einzahlung:", account1.get_balance())
    elif choice == "A":
        betrag = float(input("Betrag eingeben: "))
        account1.withdraw(betrag)
        print("Konto1: Kontoguthaben nach Abhebung:", account1.get_balance())
    elif choice == "Ü":
        betrag = float(input("Betrag eingeben: "))
        account1.transfer(account2, betrag)
        print("Konto1: Kontoguthaben nach Überweisung:", account1.get_balance())
    else:
        print("Ungültige Auswahl.")
    return choice
    


#account1.deposit(100)
#print("Konto1: Kontoguthaben nach Einzahlung:", account1.get_balance())
#account1.withdraw(30)
#print("Konto1: Kontoguthaben nach Abhebung:", account1.get_balance())
#account1.transfer(account2, 50)
#print("Konto1: Kontoguthaben nach Überweisung:", account1.get_balance())

Kontonummer = input("Kontonummer eingeben: ")
if Kontonummer == "12345":
    print("Zugriff gewährt.\n Guthaben:", account1.get_balance())
    while True:
        eingabe()
        if input("Möchten Sie eine weitere Transaktion durchführen? (Drücken Sie Enter zum Fortfahren, oder geben Sie 'q' zum Beenden ein): ").lower() == 'q':
            break
        print("Guthaben:", account1.get_balance())

elif Kontonummer == "67890":
    print("Zugriff gewährt.\n Guthaben:", account2.get_balance())
    eingabe()
else:
    print("Zugriff verweigert.")




# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.




# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


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
