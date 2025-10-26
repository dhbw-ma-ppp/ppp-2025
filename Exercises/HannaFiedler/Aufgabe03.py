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
    def __init__(self, balance):    #Konstruktor
        self._balance = balance
    
    def deposit(self, amount):      #Einzahlen
        self._balance += amount
    
    def withdraw(self, amount):     #Auszahlen
        self._balance -= amount

    def get_balance(self):          #Kontostand ausgeben
        return self._balance
    
    def transfer(self, other_account, amount):  #Auf anderes Konto überweisen
        self._balance -= amount
        other_account._balance += amount

my_account = BankAccount(2000)
other_account = BankAccount(1000)
print("Part 1:")
my_account.deposit(200)
print("Einzahlen:",my_account.get_balance())
my_account.withdraw(150)
print("Abheben:",my_account.get_balance())
my_account.transfer(other_account, 23)
print("Transfer:",my_account.get_balance(), "(my_account),", other_account.get_balance(),"(other_accout)")


# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Kartendeck:
    def __init__(self, name):       #Konstruktor
        self.deck = []    
        self._create()          #Die Liste wird automatisch mit Karten gefüllt
        self.name = name

    def _create(self):              #Das Deck soll nur über den Konstruktor aufgerufenwerden können, daher "_"
        for i in range(13): #13 verschiedene Zahlen
            for j in range(4):  #4 verschiedene Farben
                self.deck.append(Karte(i,j))
                self.deck.append(Karte(i,j))

    def __iter__(self):
        return iter(self.deck)
     
class Karte:
    def __init__(self, number, suite):  #Kosntruktor der Karte
        self.number = number
        self.suite = suite

    def __str__(self):                  #Eine lesbare Beschreibung der Karte 
        numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        suites = ["diamonds", "hearts", "spades", "clubs"]
        return f"{numbers[self.number]} of {suites[self.suite]}"
    
print("\nPart 2:")
deck1 = Kartendeck("deck1")
#print("\nIterate:") #Iterieren über alle Karten des Decks
#for card in deck1:
#    print(card)


# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class Skatdeck(Kartendeck):
    def _create(self):              #Das Deck soll nur über den Konstruktor aufgerufenwerden können, daher "_"
        for i in range(5, 13):      #Erst ab der 7
            for j in range(4):
                self.deck.append(Karte(i,j))
                self.deck.append(Karte(i,j))
        return self.deck

print("\nPart 3:")
deck2 = Skatdeck("deck2")
#print("\nSkatdeck:") #Iterieren über alle Karten des Skatdecks
#for card in deck1:
#    print(card)

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)
assert len(deck1.deck) == 104, "Das Deck sollte 104 Karten haben."  #13*4*2
assert len(deck2.deck) == 64, "Das Skatdeck sollte 64 Karten haben."#(13-5)*4*2
assert str(deck1.deck[0]) == "2 of diamonds", "An Position 0 des Decks sollte sich die Karo 2 befinden"
assert str(deck2.deck[0]) == "7 of diamonds", "An Position 0 des Skatdecks sollte sich die Karo 7 befinden"
assert str(deck1.deck[0]) == str(deck1.deck[1]), "Die erste Karte sollte doppelt vorkommen."
count = 0
for card in deck1:
    count += 1
assert count == 104, "Es sollte über 104 Karten iteriert weden."
count = 0
for card in deck2:
    count += 1
assert count == 64, "Es sollte über 64 Karten iteriert weden."
print("Alle Tests bestanden.")


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

class Number: 
    def __init__(self,lower, upper): 
        self.lower = lower 
        self.upper = str(upper)                        
        self.count = 0 
        for length in range(len(str(lower)), len(str(upper)) + 1):  #Erzeugt Liste für die Ziffern der neuen Zahl 
            self.digits = [0] * length
            self._generate(0, False, 0, 0)                          

    def _generate(self, pos, twice, prev, run_len):                 #Generiert eine Zahl, dessen Ziffern aufsteigend sind, mind. ein Paar einthält 
        if pos == len(self.digits): 
            if run_len == 2:                                        #Notwendig, wenn die letzten beiden Ziffern das Paar bilden
                twice = True
            n = int("".join(map(str, self.digits)))                 #Fügt die Ziffern zu einer Zahl zusammen 
            if self.lower <= n <= int(self.upper) and twice:        #Wenn die bedingungen erfüllt sind, wird die Anzahlt um 1 erhöht
                self.count +=1                                       
                #print(n)
            return 
        
        if pos > 0:                                                 #Bei der ersten Stelle soll ab 1 gestartet werden, sonst ab der vorherigen Ziffer
            start = prev 
        else: 
            start = 1

        for j in range(start, 10):                                  #Erzeugt Ziffer die >= ist als die vorherige 
            if j == prev:
                new_run = run_len +1                                #run_len zählt wie häufig die aktuelle Ziffer vorkommt
                new_twice = twice
            else:                                                   #Wenn sich die Ziffer ändert, beginnt das Zählen neu und es wird geprüft ob es bereits ein Paar gibt
                new_run = 1
                if twice or run_len == 2:                           
                    new_twice = True
                else:
                    new_twice = False

            self.digits[pos] = j                                    #j wird an der Stelle "pos" zur Zahl hinzugefügt
            self._generate(pos+1, new_twice, j, new_run)            #Rekursiver Aufruf 
    
    def total(self):                                                #Gibt Anzahl der Zahlen zurück 
        return self.count 

# run your function with the lower bound `13456471` and the upper bound `58515929`. 
# It should complete in a few seconds. Note the resulting count in your pull request, please.
print("\nPart 4:") 
number1 = Number(13456471, 58515929) 
print("Anzahl:",number1.total())

#Anzahl: 5234