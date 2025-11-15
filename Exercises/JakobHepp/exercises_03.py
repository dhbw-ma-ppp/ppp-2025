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
    def __init__(self, initial_balance = 0):
        if initial_balance < 0:
            raise ValueError("Du befindest dich im Minus")
        self._balance = initial_balance

    def deposit(self, amount):
        self._balance += amount
        print(f"Sie haben: {amount}€ eingezahlt")
        

    def withdraw(self, amount):
        if amount <= 0:
            print("Der Betrag muss positiv sein!")
            return False
        elif self._balance >= amount:
            self._balance -= amount
            print(f"Es wurden {amount}€ abgehoben")
            
            return True
        else:
            print(f"Sie können nicht {amount}€ abheben, da Ihr Kontostand nur {self._balance}€ beträgt")
            return False
        
    def get_balance(self):
        print(f"Ihr Kontostand beträgt: {self._balance}€")
        return self._balance
    
    def transfer(self, other_account, amount):
        
        if self.withdraw(amount):
            self.get_balance()
            other_account.deposit(amount)
            print(f"Es wurden von {id(self._balance)}  {amount}€ an {id(other_account)} gesendet")
            

        else:
            print("Es ist ein Fehler aufgetreten")


    
print("Aufgabe 1")
#Beispiele:
Konto1 = BankAccount(100)
Konto2 = BankAccount(200)
Konto1.deposit(10)
Konto1.get_balance()
print("\n")

Konto1.withdraw(10)
Konto1.get_balance()
print("\n")

Konto1.transfer(Konto2, 50)
Konto1.get_balance()
Konto2.get_balance()



# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

print(" ")
print("Aufgabe 2")



class Karte:
    def __init__(self, wert, symbol):
        self.wert = wert
        self.symbol = symbol

    def __str__(self):
        return f"{self.wert} of {self.symbol}"

    def __repr__(self):
        return str(self)
    
class Deck:
     werte = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
     symbole = ['Karo', 'Herz', 'Pik', 'Kreuz']

     def __init__(self):
        self.karten = [Karte(wert, symbol) for symbol in self.symbole for wert in self.werte]

     def __len__(self):
        return len(self.karten)

     def __getitem__(self, index):
        return self.karten[index]
    
class FrenchDeck(Deck):
    #erzeugt für jedes Symbol eine Karte mit jedem Wert, welche in einer Liste gespeichert werden
    #funktioniert, wie zwei ineinander liegende For-Schleifen
    def __init__(self):
        self.karten = [Karte(wert, symbol) for symbol in self.symbole for wert in self.werte]

    def __str__(self):
        return f"French Deck mit {len(self)} Karten."
    
    



# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


#Das Skat Deck unterscheidet sich vom French Deck nur in der Anzahl der Karten, weshalb die Definition der Werte in der SkatDeck-Klasse reichen
class SkatDeck(Deck):
    werte = [str(n) for n in range(7, 11)] + ["J", "D", "K", "A"]

    def __str__(self):
        return f"Skat Deck mit {len(self)} Karten."


#Tests:
french_deck = FrenchDeck()
print(french_deck)
print()
print(french_deck[0])
print()
print(french_deck[-1])
print()
for karte in french_deck:
   print(karte)

print("")
print("Aufgabe 3")

skat_deck = SkatDeck()
print(skat_deck)
print()
print(skat_deck[0])
print()
print(skat_deck[-1])
print()

for karte in skat_deck:
    print(karte)


assert len(french_deck) == 52
assert len(skat_deck) == 32
assert isinstance(french_deck[0], Karte)
assert str(french_deck[0]) == "2 of Karo"

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
def has_exactly_two_adjacent_same_digits(n):
    s = str(n) #-> Zahl n wird in eine Zeichenkette umgewandelt, damit man auf jede einzelne Ziffer zugreifen kann
    i = 0
    while i < len(s) - 1:
        count = 1
        while i + count < len(s) and s[i] == s[i + count]:
            count += 1
        if count == 2:
            return True
        i += count
    return False

def digits_never_decrease(n):
    s = str(n)
    return all(s[i] <= s[i + 1] for i in range(len(s) - 1)) #-> es wird geprüft, ob jede Ziffer kleiner oder gleich der nächsten Ziffer ist

def count_valid_numbers(lower, upper):
    count = 0
    for n in range(lower, upper):
        if digits_never_decrease(n) and has_exactly_two_adjacent_same_digits(n):
            count += 1
    return count

# Beispielaufruf
print(count_valid_numbers(13456471, 58515929))

#-> Output = 5234