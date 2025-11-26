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
    def __init__(self, initial_balance=0): 
        self._balance = initial_balance # privates Attribut für Kontostand

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Einzahlungsbetrag darf nicht negativ sein")
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
    if choice == "E" or choice == "e":
        betrag = float(input("Betrag eingeben: "))
        account1.deposit(betrag)
        print("Konto1: Kontoguthaben nach Einzahlung:", account1.get_balance())
    elif choice == "A" or choice == "a":
        betrag = float(input("Betrag eingeben: "))
        account1.withdraw(betrag)
        print("Konto1: Kontoguthaben nach Abhebung:", account1.get_balance())
    elif choice == "Ü" or choice == "ü":
        betrag = float(input("Betrag eingeben: "))
        account1.transfer(account2, betrag)
        print("Konto1: Kontoguthaben nach Überweisung:", account1.get_balance())
    else:
        print("Ungültige Auswahl.")
    return choice
    
print("Aufgabe 1:")

print("Konto1: Anfangskontostand:", account1.get_balance())
print("Konto2: Anfangskontostand:", account2.get_balance())
account1.deposit(100)
print("Konto1: Kontoguthaben nach Einzahlung:", account1.get_balance())
account1.withdraw(30)
print("Konto1: Kontoguthaben nach Abhebung:", account1.get_balance())
account1.transfer(account2, 50)
print("Konto1: Kontoguthaben nach Überweisung:", account1.get_balance())
print("Konto2: Kontoguthaben nach Überweisung:", account2.get_balance())


#Kontonummer = input("Kontonummer eingeben: ")
#if Kontonummer == "12345":
#   print("Zugriff gewährt.\n Guthaben:", account1.get_balance())
#  while True:
#        eingabe()
 #       if input("Möchten Sie eine weitere Transaktion durchführen? (Drücken Sie Enter zum Fortfahren, oder geben Sie 'q' zum Beenden ein): ").lower() == 'q':
 #           break
 #       print("Guthaben:", account1.get_balance())

#elif Kontonummer == "67890":
#    print("Zugriff gewährt.\n Guthaben:", account2.get_balance())
#    eingabe()
#else:
#    print("Zugriff verweigert.")



# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Card:
    SUITS = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, rank): 
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}" 


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def __getitem__(self, index): 
        return self.cards[index] 

    def __iter__(self):
        return iter(self.cards) # Gibt einen Iterator über die Karten im Deck zurück

    def __len__(self):
        return len(self.cards) # Gibt die Anzahl der Karten im Deck zurück

    def __str__(self):
        return ", ".join(str(card) for card in self.cards) # Gibt eine lesbare Darstellung des gesamten Decks zurück
# Beispiel:
deck = Deck()
print("\nAufgabe 2:")
print("Ausgabe des gesamten Decks:", deck) # Ausgabe aller Karten im Deck
print("Erste Karte im Deck:", deck[0]) # Ausgabe der ersten Karte im Deck
print("\nAlle Karten im Deck:")
for card in deck:
    print(card)  # Ausgabe jeder Karte im Deck einzeln


# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
# using built-in assert instead of external 'assertpy'

class SkatDeck(Deck):
    def __init__(self):
        super().__init__()  # Rufe den Konstruktor der Basisklasse auf
        self.cards = [card for card in self.cards if Card.RANKS.index(card.rank) >= Card.RANKS.index('7')]  # Filtere Karten ab 7 aufwärts

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
#Tests:
skat_deck = SkatDeck()
print("\nAufgabe 3:")
print("Ausgabe des gesamten Skat-Decks:", skat_deck) # Ausgabe aller Karten im Skat-Deck
print("Erste Karte im Skat-Deck:", skat_deck[0]) # Ausgabe der ersten Karte im Skat-Deck
print("\nAlle Karten im Skat-Deck:")
for card in skat_deck:
    print(card)  # Ausgabe jeder Karte im Skat-Deck einzeln

print("\nAnzahl der Karten im normalen Deck:", len(deck))  # Anzahl der Karten im normalen Deck
print("Anzahl der Karten im Skat-Deck:", len(skat_deck))
assert len(deck) == 52  # Normales Deck sollte 52 Karten haben
assert len(skat_deck) == 32  # Skat-Deck sollte 32 Karten haben


# PART 4:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right

def count_valid_numbers(lower_bound, upper_bound):  #Zählt gültige Zahlen im Bereich
    valid_count = 0 

    for number in range(lower_bound, upper_bound):  
        str_num = str(number)   # Zahl in String umwandeln
        
        # prüfen, ob die Ziffern nur zunehmen
        if any(str_num[i] > str_num[i+1] for i in range(len(str_num)-1)):
            continue

        # prüfen, ob es mindestens eine Gruppe von genau zwei benachbarten Ziffern gibt
        has_exactly_two_adjacent = False
        i = 0
        while i < len(str_num):     
            count = 1
            while i + 1 < len(str_num) and str_num[i] == str_num[i + 1]:    # Zähle gleiche benachbarte Ziffern
                count += 1
                i += 1
            if count == 2:  # genau zwei benachbarte Ziffern gefunden
                has_exactly_two_adjacent = True     
                break
            i += 1
        
        if has_exactly_two_adjacent:
            valid_count += 1 # gültige Zahl gefunden

    return valid_count

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
print("\nAufgabe 4: dauert einen Moment...")
result = count_valid_numbers(13456471, 58515929)
print("Anzahl der gültigen Zahlen im Bereich:", result)


