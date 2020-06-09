import pydealer as pd
import inspect
from pydealer import Card


kozer = 'Diamonds'
def main():
	deck = createDurakDeck()
	hands = list()
	deck.shuffle()

	# test CheckBeats
	beat_card = deck[26]
	print("beat Card is", beat_card)
	for card in deck:
		if checkBeats(card, beat_card, kozer):
			print(beat_card, "beats", card)
		
		
		


def playARound(attacker, defender, kozer_suit):
	print("welcome! kozer = ", kozer_suit)

	# internal variable to store 'not-yet-defended' cards on the table
	_cardsToDefend = pd.stack.Stack()

	# attacker attacks
	print(attacker.name, "- select card to attack with:")
	print("\n//////////", attacker.name, "////////// ATTACK //////////", defender.name, "//////////")
	_cardsToDefend = attacker.attack()

	# defender defends
	print("\n//////////", defender.name, "////////// DEFEND //////////", attacker.name, "//////////")
	while(len(_cardsToDefend) > 0):
		# defender selects card_to_defend and card_to_defend_with
		card_to_def, card_to_def_with = defender.defend(_cardsToDefend)
		
		print("right before armageddon, type(card_to_def) =", type(card_to_def))
		print("right before armageddon, card_to_def =", card_to_def)
		
		if type(card_to_def) == list:
			card_to_def = card_to_def[0]
		card_to_def_with = card_to_def_with[0]

		# TODO: check if cards actually beats
		if checkBeats(card_to_def, card_to_def_with, kozer_suit):
			# remove card_to_def from _cardsToDefend
			_cardsToDefend.remove(card_to_def)
			print(defender.name, "succesfully defends the ", card_to_def, "with the", card_to_def_with)

			# remove card - this can be a function later hand.remove(card)
			defender.hand = list(defender.hand)
			defender.hand.remove(card_to_def_with)
		else:
			print("\n|!|!|!|!|!|!|THAT DOESNT WORK FOOL||||||||||||\n")
			print("you cant beat the", card_to_def, "with the", card_to_def_with)
		


class Player:
	def __init__(self, name, hand):
		self.name = name
		self.hand = hand

	def attack(self):
		# attack with any card
		attack_cards = selectCards(self.name, self.hand, "to attack with")
		return attack_cards

	def defend(self, hand):
		# remind player of their hand
		durakSort(self.hand)
		print("Time to Defend", self.name, "your hand is:\n")
		print(self.hand, '\n')

		# select card to defend
		card_to_defend = selectCards(self.name, hand, "to defend")
		
		#select card to defend with
		strCat = "to defend the [" + str(card_to_defend) + "] with "
		card_to_defend_with = selectCards(self.name,self.hand, strCat)

		# return both
		return(card_to_defend, card_to_defend_with)
		
def selectCards(name, stack, msg_append = "", take=False):
	if (len(stack) == 1):
		return stack[0]
	
	returnList = []
	message = "Select a card " + msg_append
	print(message, name)
	durakSort(stack)
	for i in range(len(stack)):
		print(i, ":", stack[i])
	user_input = input("Enter Selection (number, space seperated for multiple) here: ")
	print("Excelent Choice! You selected:")
	if (user_input.lower() == 'take'):
		print("ok yo takin")
		# user.takes()fucntoin
	for selection in user_input.split():
		returnList.append(stack[int(selection)])
		print(stack[int(selection)])
	return returnList

def checkBeats(atkCard, defCard, kozer):
	if (atkCard.suit == defCard.suit):
		return atkCard.value < defCard.value
	else:
		return (defCard.suit == kozer) and (defCard.value > atkCard.value or atkCard.suit != kozer)
def durakSort(stack):
	kozers = []
	stack.sort()
	for card in stack:
		if (card.suit == kozer):
			kozers.append(stack.get(stack.find(str(card))[0]))
	for k in kozers:
		stack.add(k)

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]
 
def mod_retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]

def createDurakDeck():
	deck_ = pd.Deck()
	deck_.empty()
	deck_.add([Card(value='6', suit='Diamonds'), Card(value='6', suit='Clubs'), Card(value='6', suit='Hearts'), Card(value='6', suit='Spades'), Card(value='7', suit='Diamonds'), Card(value='7', suit='Clubs'), Card(value='7', suit='Hearts'), Card(value='7', suit='Spades'), Card(value='8', suit='Diamonds'), Card(value='8', suit='Clubs'), Card(value='8', suit='Hearts'), Card(value='8', suit='Spades'), Card(value='9', suit='Diamonds'), Card(value='9', suit='Clubs'), Card(value='9', suit='Hearts'), Card(value='9', suit='Spades'), Card(value='10', suit='Diamonds'), Card(value='10', suit='Clubs'), Card(value='10', suit='Hearts'), Card(value='10', suit='Spades'), Card(value='Jack', suit='Diamonds'), Card(value='Jack', suit='Clubs'), Card(value='Jack', suit='Hearts'), Card(value='Jack', suit='Spades'), Card(value='Queen', suit='Diamonds'), Card(value='Queen', suit='Clubs'), Card(value='Queen', suit='Hearts'), Card(value='Queen', suit='Spades'), Card(value='King', suit='Diamonds'), Card(value='King', suit='Clubs'), Card(value='King', suit='Hearts'), Card(value='King', suit='Spades'), Card(value='Ace', suit='Diamonds'), Card(value='Ace', suit='Clubs'), Card(value='Ace', suit='Hearts'), Card(value='Ace', suit='Spades')])
	return deck_
if __name__ == "__main__":
	main()
