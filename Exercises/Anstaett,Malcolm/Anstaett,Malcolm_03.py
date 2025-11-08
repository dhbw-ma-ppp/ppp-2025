# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.

print("Aufgabe 1:\n")

class BankAcount:

    def __init__(self,owner): # __init__ Methode für Bankkonto
        self.owner = owner
        self._balance = 0

    def deposit(self, amount): # Einzahlungsmethode
        self._balance += amount
        print(f"Einzahlung von: {amount}\n. Neuer Kontostand: {self._balance}.")

    def withdraw(self, amount): # Auszahlungsmethode
        if amount > self._balance:
            print("Kontostand nicht ausreichend.")
        else:
            self._balance -= amount
            print(f"Auszahlung von: {amount}\n. Neuer Kontostand: {self._balance}.")
    
    def get_balance(self): # Kontostand abrufen
        return self._balance
    
    def transfer(self,amount, owner): # Überweisung
        if amount > self._balance:
            print("Kontostand nicht ausreichend.")
        else:
            self._balance -= amount
            owner._balance += amount
            print(f"Überweisung von: {amount} an Konto: {owner.owner}\n. Neuer Kontostand: {self._balance}.")

#Funktionstest

account1 = BankAcount("Max Mustermann")
account2 = BankAcount("Erika Mustermann")

account1.deposit(1000)
account1.withdraw(200)
account1.transfer(300, account2)

print(f"Konto 1 Kontostand: {account1.get_balance()}")
print(f"Konto 2 Kontostand: {account2.get_balance()}\n")




# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

print("Aufgabe 2:\n")

class french_deck:

    def __init__(self): # __init__ für französisches Deck
        suites = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [f"{value} of {suite}" for suite in suites for value in values]

    def get_card(self, position): # Karte an bestimmter Position abrufen
        print(self.cards[position])

    def __iter__(self): # Iteration über alle Karten im Deck ermöglichen
        for card in self.cards:
            yield card


deck = french_deck()
deck.get_card(0)  # Ausgabe: Spezifische Karte 

# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

print("Aufgabe 3:\n")

class skat_deck(french_deck):

    def __init__(self): # __init__ für Skat-Deck überschreiben mit Werten von 7 bis Ass
        suites = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        values = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [f"{value} of {suite}" for suite in suites for value in values]

skat = skat_deck()
skat.get_card(0)  # Ausgabe: Spezifische Karte


# Test FrenchDeck
assert len(french_deck) == 52 # Prüfen ob das französische Deck 52 Karten hat
assert str(french_deck[0]) == "2 of Diamonds" # Prüfen ob die erste Karte korrekt ist
assert str(french_deck[-1]) == "Ace of Clubs" # Prüfen ob die letzte Karte korrekt ist


# Test SkatDeck
assert len(skat_deck) == 32 # Prüfen ob das Skat-Deck 32 Karten hat
assert str(skat_deck[0]) == "7 of Diamonds" # Prüfen ob die erste Karte korrekt ist
assert str(skat_deck[-1]) == "Ace of Clubs" # Prüfen ob die letzte Karte korrekt ist

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

import time

print("Aufgabe 4:\n")

def specific_number_counter(lower_bound, upper_bound):
    
    def has_exactly_double(num_str):  # Prüfe, ob es eine Gruppe von genau zwei gleichen Ziffern gibt
        group_size = 1
        for i in range(1, len(num_str)): # Ziffern durchlaufen
            if num_str[i] == num_str[i - 1]: # Überprüfen ob die Ziffern gleich sind
                group_size += 1 
            else:
                if group_size == 2:  # Gruppe von genau zwei gefunden
                    return True
                group_size = 1
        return group_size == 2   # Letzte Gruppe überprüfen

    def digits_increase(num_str): # Prüfe, ob die Ziffern nur ansteigen
        for i in range(len(num_str) - 1): # Ziffern durchlaufen
            if num_str[i] > num_str[i + 1]: #Vergleichen und schauen ob die Ziffern ansteigen
                return False
        return True

    count = 0
    for num in range(lower_bound, upper_bound):
        num_str = str(num)  # Einmalige String-Konvertierung
        if digits_increase(num_str):  # Funktion aufrufen um zu prüfen ob die Ziffern ansteigen
            if has_exactly_double(num_str):  # Funktion aufrufen um zu prüfen ob es eine Gruppe von genau zwei gleichen Ziffern gibt
                count += 1
    return count

# Start Timer
start_time = time.time()

# Funktion ausführen
result = specific_number_counter(13456471, 58515929)

# Stop Timer
end_time = time.time()

# Ergebnis und Zeit ausgeben
print(f"Ergebnis1: {result}") # Ausgabe des Ergebnisses: 5234
print(f"Berechnungszeit: {end_time - start_time:.2f} Sekunden") # Ausgabe der Zeit in Sekunden