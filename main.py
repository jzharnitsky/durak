import pydealer as pd
import inspect
from pydealer import Card


kozer = 'Diamonds'
def main():
	# initialize stuff - can be put in init() later
	deck = createDurakDeck()
	discard = list() # TODO: implement
	hands = list()
	deck.shuffle()

	# deal 4 hands
	for i in range(4):
	    hands.append(deck.deal(6))

	# assign a player to each hand
	josh = Player("josh", hands[0])
	manny = Player("manny", hands[1])
	nua = Player("nua", hands[2])
	adam = Player("adam", hands[3])

	# plays a round, changes everyones hand + discard + deck accordingly
	playARound(josh, nua, kozer)

	print("\n------ After playARound --------\n")
	print("joshs hand is now:")
	printHand(josh.hand)
	print("nuas hand is now:")
	printHand(nua.hand)
	


def playARound(attacker, defender, kozer_suit):
	print("welcome! kozer = ", kozer_suit)

	# internal variables
	_cardsToDefend = pd.stack.Stack()
	_buffer = pd.stack.Stack()

	# attacker attacks
	print(attacker.name, "- select card to attack with:")
	print("\n//////////", attacker.name, "////////// ATTACK //////////", defender.name, "//////////")
	_cardsToDefend = attacker.attack()

	# defender defends until no more cards to defend
	print("\n//////////", defender.name, "////////// DEFEND //////////", attacker.name, "//////////")
	while(len(_cardsToDefend) > 0):
		# defender selects card_to_defend and card_to_defend_with (or take)
		card_to_def, card_to_def_with = defender.defend(_cardsToDefend)

		# check if user took
		if (card_to_def == 'take'):
			defender.take(_buffer + _cardsToDefend)
			_cardsToDefend = []
			return
		
		print("right before armageddon, type(card_to_def) =", type(card_to_def))
		print("right before armageddon, card_to_def =", card_to_def)
		
		if type(card_to_def) == list:
			card_to_def = card_to_def[0]
		card_to_def_with = card_to_def_with[0]

		# TODO: check if cards actually beats
		if checkBeats(card_to_def, card_to_def_with, kozer_suit):
			# remove card_to_def from _cardsToDefend and add to buffer
			_cardsToDefend.remove(card_to_def)
			_buffer.add(card_to_def)

			# print success message
			print("/////////// ", end='')
			print(defender.name, "succesfully defends the ", card_to_def, "with the", end='')
			print(card_to_def_with," \\\\\\\\\\\\\\\\\\\\\\")

			# remove card - this can be a function later hand.remove(card)
			defender.hand = list(defender.hand)
			defender.hand.remove(card_to_def_with)
		else:
			print("\n|!|!|!|!|!|!|THAT DOESNT WORK FOOL||||||||||||\n")
			print("you cant beat the", card_to_def, "with the", card_to_def_with)
		
	# _cardsToBeat is empty
	

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
		self.hand = durakSort(self.hand)
		print("Time to Defend", self.name, "your hand is:\n")
		printHand(self.hand, "\n")

		# select card to defend
		card_to_defend = selectCards(self.name, hand, "to defend (OR 'take' TO TAKE)")

		# check if user took
		if ((card_to_defend == 'take') or (card_to_defend_with == 'take')):
			return ('take', 'take')
		
		#select card to defend with
		strCat = "to defend the [" + str(card_to_defend) + "] with (OR 'take' TO TAKE)"
		card_to_defend_with = selectCards(self.name,self.hand, strCat)
		
		# check if user took
		if ((card_to_defend == 'take') or (card_to_defend_with == 'take')):
			return ('take', 'take')

		# return if user defended successfully
		return(card_to_defend, card_to_defend_with)
	
	def take(self, junk):
		self.hand.append(junk)

def printHand(hand, arg1='', arg2='', arg3=''):
	for card in hand:
		print(card)
	print(arg1, arg2, arg3)
		
def selectCards(name, stack, msg_append = "", take=False):
	returnList = [] 
	# if one item in list return item
	if (len(stack) == 1):
		return stack[0]

	# print stuff
	message = "Select a card " + msg_append
	print(message, name)
	stack = durakSort(stack)
	for i in range(len(stack)):
		print(i, ":", stack[i])

	# collect user input
	user_input = input("Enter Selection (number, space seperated for multiple) here: ")

	# return user selection
	print("Excelent Choice! You selected:")
	if (user_input.lower() == 'take'):
		print("TO TAKE U LOZER")
		return "take"
	for selection in user_input.split():
		returnList.append(stack[int(selection)])
		print(stack[int(selection)])
	return returnList

def checkBeats(atkCard, defCard, kozer):
	if (atkCard.suit == defCard.suit):
		return atkCard.lt(defCard)
	else:
		return (defCard.suit == kozer) and (defCard.gt(atkCard) or atkCard.suit != kozer)

def durakSort(arr):
	# sort kozers and nonKozers seperately
	kozers = []
	nonKozers = []
	for card in arr:
		if (card.suit == kozer):
			kozers.append(card)
		else:
			nonKozers.append(card)
			
	kozers = quickSort(kozers)
	nonKozers = quickSort(nonKozers)

	return nonKozers + kozers

def quickSort(arr):
	if (len(arr) <=1):
		return arr
	else:
		return quickSort( [x for x in arr[1:] if x.lt(arr[0])] ) + \
			[arr[0]] + \
			quickSort([x for x in arr[1:] if x.gt(arr[0])])

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
