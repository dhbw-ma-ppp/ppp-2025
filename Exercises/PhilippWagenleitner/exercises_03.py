# PART 1:
# Create a class BankAccount with:
# A “private” attribute _balance
# Methods:
#  deposit(amount) → increases the balance
#  withdraw(amount) → decreases it (if enough funds)
#  get_balance() → returns the balance
#  transfer(other_account, amount) -> It should withdraw from one account and deposit into the other.
#  Try depositing, withdrawing and transferring amounts and print the balance each time.

def declare_amount():
    try:
        amount = float(input("Geben Sie den Betrag ein: "))
        if amount <= 0:
            print("Der Betrag muss positiv sein.")
            return 0
        return amount
    except ValueError:
        print("Kein richtiger Betrag eingegeben\nAbbruch...")
        return 0

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance
        
    def deposit(self, amount):
        print("Einzahlung...")
        self.__balance += amount
        return True 
        
    def withdraw(self, amount): 
        if self.__balance - amount < 0:
            print("\nNicht genug Geld vorhanden.")
            return False
        else:
            print("Auszahlung...")
            self.__balance -= amount
            return True

    def get_balance(self):
        print(f"\nAktueller Kontostand: {self.__balance}€")
    
    def transfer(self, amount, target_account):
        if self.withdraw(amount): 
            print("\nÜberweisung...")
            target_account.deposit(amount) 
            print(f"Überweisung von {amount}€ an das andere Konto erfolgreich.")
            return True
        else:
            print("Überweisung fehlgeschlagen.")
            return False

if __name__ == '__main__':
    print("Teil 1:")
    print("Startbetrag einzahlen")
    
    start_amount = declare_amount()
    
    mein_konto = BankAccount(start_amount)
    other_account = BankAccount(0)
    
    mein_konto.get_balance()
    
    while True:
        print("-" * 20)
        print("Wählen Sie Ihre Aktion:")
        print("(1) - Kontostand anschauen")
        print("(2) - Einzahlen")
        print("(3) - Auszahlen")
        print("(4) - Überweisung auf anderes Konto")
        print("(q) - Abbruch")
        auswahl = input("Aktion: ")

        match auswahl:
            case '1':
                mein_konto.get_balance()
            case '2':
                amount = declare_amount()
                mein_konto.deposit(amount)
                mein_konto.get_balance()
            case '3':
                amount = declare_amount()
                mein_konto.withdraw(amount)
                mein_konto.get_balance()
            case '4': 
                amount = declare_amount()
                mein_konto.transfer(amount, other_account) 
                
                print("--- Übersicht nach Transfer ---")
                print("\nMein Kontostand:")
                mein_konto.get_balance()
                print("\nAnderes Konto Kontostand:")
                other_account.get_balance()
            case 'q':
                print("Abbruch...")
                break
            case _:
                print("\nFehlerhafte Eingabe!")

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.


def create(color, number):
        card=[]
        for i in range (len(number)):
            for j in range(len(color)):
                card.append(number[i]+" of "+color[j])
        return card

class cards:
    def __init__(self, color, number):
        self.color=color
        self.number=number
        self.deck=create(color, number)
    def retrieve_card(self):
        try:
            index=int(input("Geben sie den Index einer Karte ein: "))
            print(f"Die Karte am Index {index} ist:\n'{self.deck[index]}'\n")
        except ValueError, IndexError:
            print("Fehlerhafte Eingabe! (Index zu hoch oder keine Zahl eingegeben)")
            print(f"(Max. Index {len(self.deck)-1} | {len(self.deck)} Karten im Deck)\n")

if __name__=='__main__':
    print("\nTeil 2 - French-Deck: \n")
    french_number=[str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
    color=["Diamonds", "Hearts", "Spades", "Clubs"]
    french_deck=cards(color, french_number)
    while True:
        print("Aktionen:\n(1)-Karte ausgeben\n(q)-Quit")
        choice=input("Input: ")
        match choice:
            case '1':
                french_deck.retrieve_card()
            case 'q':
                print("quit...")
                break
            case _:
                print("Ungültige Aktion!\n")
                continue

    print("\nTeil 3 - Skat-Deck:\n")
    skat_numbers=[str(n) for n in range(7, 11)] + ["J", "Q", "K", "A"]
    skat_deck=cards(color, skat_numbers)
    while True:
        print("Aktionen:\n(1)-Karte ausgeben\n(q)-Quit")
        choice=input("Input: ")
        match choice:
            case '1':
                skat_deck.retrieve_card()
            case 'q':
                print("quit...\n")
                break
            case _:
                print("Ungültige Aktion!\n")
                continue


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

import time

def validate(lower, upper):  
    count=0 
    lower+=1 
    while upper>lower:
        temp_str=str(lower)
        if condition_1(temp_str):
            if condition_2(temp_str):
                lower+=1
                count+=1
            else:
                lower+=1
                continue
        else: 
            lower+=1
            continue
    return count

def condition_2(temp_str): #Prüfen auf Paar
    length = len(temp_str)
    for i in range(length - 1):
        if temp_str[i] == temp_str[i+1]:
            group_of_three = (i + 2 < length) and (temp_str[i+2] == temp_str[i]) 
            part_of_previous = (i > 0) and (temp_str[i-1] == temp_str[i]) 
            if not group_of_three and not part_of_previous: 
                return True 
    return False

    
def condition_1(temp_str): #Prüfen ob Ziffern von links nach rechts steigen
    boolean=True
    for l in range(len(temp_str) -1):
        if temp_str[l]<=temp_str[l+1]: 
                boolean=True
                continue
        else: 
            boolean=False
            break
    return boolean
        
if __name__=='__main__':
    print("Teil 4:\n")
    lower=13456471
    upper=58515929
    time_before=time.time()
    count=validate(lower, upper)
    time_after=time.time()
    print(f"There are {count} numbers in between {lower} and {upper}!\n")
    print(f"Time needed: {time_after-time_before:.4f}s")