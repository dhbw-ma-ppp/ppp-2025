print("Aufgabe1:")

class BankAccount:
    
    def __init__(self, balance):
        self.__balance = balance  # private Variable

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{amount} € eingezahlt. Neuer Kontostand: {self.__balance} €")
            return True
        else:
            print("Betrag muss positiv sein!")
            return False

    def withdraw(self, amount):
        if amount <= 0:
            print("Der Betrag muss größer als 0 sein!")
            return False
        elif amount > self.__balance:
            print("Nicht genügend Guthaben!")
            return False
        else:
            self.__balance -= amount
            print(f"{amount} € abgehoben. Neuer Kontostand: {self.__balance} €")
            return True

    def get_balance(self):
        return self.__balance

    def transfer(self, other_account, amount):
        print(f"Überweise {amount} € auf ein anderes Konto")
        if amount <= 0:
            print("Der Betrag muss positiv sein!")
            return False
        elif self.__balance < amount:
            print("Nicht genügend Guthaben für die Überweisung!")
            return False
        else:
            self.withdraw(amount)
            other_account.deposit(amount)
            print("Überweisung erfolgreich.")
            return True

# Test
konto1 = BankAccount(200)
konto2 = BankAccount(700)

# Test Überweisung (mehr als Kontostand)
#konto1.transfer(konto2, 400)

# Test Überweisung (gültig)
#konto1.transfer(konto2, 150)

# Test Abhebung
#konto2.withdraw(100)

# Test Einzahlung
#konto1.deposit(50)

# Kontostände ausgeben
print(f"Kontostand Konto1: {konto1.get_balance()} €")
print(f"Kontostand Konto2: {konto2.get_balance()} €")





print(" ")
print("Aufgabe2: ")

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Deck:
    def __init__(self): 
        self.values = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
        self.suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        self.cards = [] # Liste aller Karten 

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]
    

class French(Deck):
    def __init__(self):
        super().__init__() # Erbt die Methoden von der Super Klasse 

        for s in self.suits:
            for v in self.values:
                self.cards.append((s,v))

deck_French = French()
print(deck_French[0])

#for card in deck_French[:5]:
    #print(card)



print(" ")
print("Aufgabe3:")
# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class Skat(Deck):
    def __init__(self):
        super().__init__()
        skat = self.values[5:]
        for s in skat:
            for v in self.suits:
                self.cards.append((s,v))
deck_Skat = Skat()
print(deck_Skat[9])
#for c in deck_Skat: # optional
    #print(len(c))
# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)



print(" ")
print("Aufgabe4: ")

# PART 4:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right
class Function:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
    
    def validnr(self):
        valid = []
        for num in range(self.lower, self.upper):
            s = str(num)
            num_waechst = True
    
           # if any(int(s[i]) > int(s[i+1]) for i in range(len(s)-1)):
               # continue
            for i in range(len(s)-1):
                if int(s[i]) > int(s[i+1]):
                    num_waechst = False
                    break
            if not num_waechst:
                continue
            

            gleich = []
            i = 0
            while i < len(s):
                Anz_gleichezahlen = 1

                while i+Anz_gleichezahlen < len(s) and s[i] == s[i+Anz_gleichezahlen]:
                    Anz_gleichezahlen += 1

                gleich.append(Anz_gleichezahlen)
                i += Anz_gleichezahlen
            
            
            if 2 in gleich:
                valid.append(num)
        
        return valid


ex = Function(13456471,58515929)
valisnums= ex.validnr()
print(f" Länge von der Upper-,Lowerbound: {len(valisnums)}")
# print(valisnums) # optional


# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `13456471` and the upper bound `58515929`. 
# It should complete in a few seconds. Note the resulting count in your pull request, please.
