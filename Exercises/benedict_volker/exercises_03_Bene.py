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
    def __init__(self):
        self._account_balance = 0
    def deposit(self, amount):
        if amount > 0:
            self._account_balance += amount
        else:
            print("The inserted amount was negative")
            raise ValueError
    def withdraw(self, amount):
        if self._account_balance >= amount and amount > 0:
            self._account_balance -= amount
        else:
            print(f"you do not have enough balance: {self._account_balance} Euro, or the requested amount was negative")
            raise ValueError
    def get_balance(self):
        return self._account_balance
    def transfer(self, other_account, amount):
        if amount > 0:
            try: 
                self.withdraw(amount)
            except ValueError:
                print("transfer failed")
                return 
        else:
            print("The inserted amount was negative")
            raise ValueError
        other_account.deposit(amount)

#Tests
acc1 = BankAccount()
acc2 = BankAccount()

acc1.deposit(100)
acc2.deposit(20)
print(acc1.get_balance(), acc2.get_balance())

acc1.transfer(acc2, 120)
print(acc1.get_balance(), acc2.get_balance())

# PART 2:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
#   The deck of cards should behave like a sequence.
#   When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
#   I should be able to index into the deck to retrieve one card.
#   I should be able to iterate over all cards in the deck.
#   Printing a cards string representation should give me a nice, readable description of that card.

class Deck:
    def __init__(self):
        self.cards = self.CARDS

    def __getitem__(self, cardindex: int):
        if cardindex > len(self.cards) or cardindex < 0:
            print("Index nicht im Kartendeck enthalten. Er muss zwischen 0 und 51 liegen")
            return 
        
        return self.cards[cardindex]
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def give_whole_deck(self):
        return self.cards
       

class CardDeck(Deck):
    CARDS = ["2 \u2666","3 \u2666","4 \u2666","5 \u2666","6 \u2666","7 \u2666","8 \u2666","9 \u2666","10\u2666","B \u2666","D \u2666","K \u2666","A \u2666",
                      "2 \u2665","3 \u2665","4 \u2665","5 \u2665","6 \u2665","7 \u2665","8 \u2665","9 \u2665","10\u2665","B \u2665","D \u2665","K \u2665","A \u2665",
                      "2 \u2660","3 \u2660","4 \u2660","5 \u2660","6 \u2660","7 \u2660","8 \u2660","9 \u2660","10\u2660","B \u2660","D \u2660","K \u2660","A \u2660",
                      "2 \u2663","3 \u2663","4 \u2663","5 \u2663","6 \u2663","7 \u2663","8 \u2663","9 \u2663","10\u2663","B \u2663","D \u2663","K \u2663","A \u2663"]
    



# PART 3:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(Deck):
    CARDS = ["2 \u2666","3 \u2666","4 \u2666","5 \u2666","6 \u2666","7 \u2666","8 \u2666","9 \u2666","10\u2666","B \u2666","D \u2666","K \u2666","A \u2666",
                      "2 \u2665","3 \u2665","4 \u2665","5 \u2665","6 \u2665","7 \u2665","8 \u2665","9 \u2665","10\u2665","B \u2665","D \u2665","K \u2665","A \u2665",
                      "2 \u2660","3 \u2660","4 \u2660","5 \u2660","6 \u2660","7 \u2660","8 \u2660","9 \u2660","10\u2660","B \u2660","D \u2660","K \u2660","A \u2660",
                      "2 \u2663","3 \u2663","4 \u2663","5 \u2663","6 \u2663","7 \u2663","8 \u2663","9 \u2663","10\u2663","B \u2663","D \u2663","K \u2663","A \u2663"]

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

deck1 = CardDeck()
print(f"You have picked the {deck1[4]}")
print(f"Das Deck besteht aus: {deck1.give_whole_deck()}")

skatdeck1 = SkatDeck()
print(f"You have picked the {skatdeck1[0]}")
print(f"Das Deck besteht aus: {skatdeck1.give_whole_deck()}")

res = "6 \u2666"
assert res == deck1[4]
assert "2 \u2666" == skatdeck1[0]

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

def check_number_pairs(num: str) -> bool:
    for char_index in range(len(num) -2):
        # Check if the first two numbers are the same and the third is different
        if num[char_index] == num[char_index +1] and num[char_index] != num[char_index +2]:
            # Check wether the number before is the same
            if char_index >= 1 and num[char_index] != num[char_index -1]:
                return True
    # Check first three numbers
    if num[0] == num[1] and num[2] != num[1]:
        return True    
    # Check the last three numbers 
    if num[-1] == num[-2] and num[-3] != num[-1]:
        return True
    return False

def set_to_next_higher_increasing_number(num: str) -> str:
    for char_index in range(len(num)-1):
        if int(num[char_index]) > int(num[char_index+1]):
            num = num[:char_index] + (len(num)-char_index)*num[char_index]
    return num

def count_matching_numbers(lower_count: int, upper_count: int) -> int:
    matching_numbers_count = 0
    number = lower_count
    while number <= upper_count:
        number = str(number)
        number = set_to_next_higher_increasing_number(number)
        if check_number_pairs(number) == True:
            matching_numbers_count += 1
        number = int(number) + 1
    return matching_numbers_count

print(f"Es gibt {count_matching_numbers(13456471,58515929)} passende Zahlen") # Ergebnis 5234
