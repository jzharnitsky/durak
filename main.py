import pydealer as pd
import inspect
from pydealer import Card
# TODO: implement 'adding' cards
kozer = 'Diamonds'

def main():
	# create players, deck, discard
	josh, manny, nua, adam, kozer, deck, discard = initGame()

	# play a game, returns 'winner'
	winner = playAGame(josh, nua, kozer, deck)
	print("Game Over! Winner was", winner.name)

def playAGame(attacker, defender, kozer, deck, discard=list(), messages=True):
	while(True):
		# plays a round, changes everyones hand + discard accordingly
		playARound(attacker, defender, kozer, discard)

		# take, changes everyones hands and deck accordingly
		take((attacker, defender), deck, 6)
		
		# See if someone won, and return winner
		if ((len(deck) == 0) and (len(attacker.hand) <= 1)):
			return attacker

		if ((len(deck) == 0) and (len(defender.hand)== 0)):
			return defender

		# some messages
		print("\n\n------ After Round --------\n")
		print(attacker.name,"hand is now:", attacker.prettyHand())
		print(defender.name, "hand is now:",defender.prettyHand())
		print("\nlen(deck) is now:", len(deck))
		print("discard = ", discard)

		# switch places
		if not (defender.justTook()):
			temp = attacker
			attacker = defender
			defender = temp
		else:
			print("~~~~~~ Defender took, so attacker attacks again ~~~~~~")
			defender.set_justTook(False)

def initGame():
	# initialize stuff
	deck = createDurakDeck()
	discard = list()
	hands = list()
	deck.shuffle()
	kozer = 'Diamonds'

	# deal 4 hands
	for i in range(4):
	    hands.append(deck.deal(6))

	# assign a player to each hand
	josh = Player("josh", hands[0])
	manny = Player("manny", hands[1])
	nua = Player("nua", hands[2])
	adam = Player("adam", hands[3])

	return josh, manny, nua, adam, kozer, deck, discard

def take(players, deck, sizeFullHand):
	for player in players:
		while( len(player.hand) < sizeFullHand):
			if (len(deck) > 0):
				player.take(deck.deal(1))
			else:
				print("DECK IS NOW EMPTY")
				return

def playARound(attacker, defender, kozer_suit, discard):
	print("welcome! kozer = ", kozer_suit)

	# internal variables
	_buffer = [] # stores the rest of the cards played

	# attacker's initial attack
	print("\n//////////", attacker.name, "////////// ATTACK //////////", defender.name, "//////////")
	print(attacker.name, "- select card to attack with:")
	_cardsToDefend = attacker.attack()

	# defender defends until no more cards to defend
	print("\n//////////", defender.name, "////////// DEFEND //////////", attacker.name, "//////////")
	while(len(_cardsToDefend) > 0):
		# defender selects 'take', or card_to_defend and card_to_defend_with 
		card_to_def, card_to_def_with = defender.defend(_cardsToDefend)

		# check if defender took
		if (card_to_def == 'take'):
			defender.take(_buffer)
			defender.take(_cardsToDefend)
			_cardsToDefend = []
			defender.set_justTook(True)
			return 
			
		# bug fixing
		if type(card_to_def) == list:
			card_to_def = card_to_def[0]
		card_to_def_with = card_to_def_with[0]

		# Check if cards actually beats
		if checkBeats(card_to_def, card_to_def_with, kozer_suit):

			# remove cards from hand and _cardsToDefend and add to buffer
			list(defender.hand).remove(card_to_def_with)
			_cardsToDefend.remove(card_to_def)
			_buffer.append(card_to_def)
			_buffer.append(card_to_def_with)

			# print success message
			print("/////////////// ", end='')
			print(defender.name, "succesfully defends the [" + str(card_to_def) + "] with the ", end='')
			print("[" + str(card_to_def_with) + "]"," \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")

			# attacker optionally add cards
			print("DEFENDER (" + defender.name.upper() + ") CARD COUNT:", defender.lengthHand())
			cardsToAdd = attacker.addCards(_buffer + _cardsToDefend)
			for card in cardsToAdd:
				_cardsToDefend.append(card)
					
		else: # else for 'if (checkBeats):'
			print("\n|!|!|!|!|!|!|THAT DOESNT WORK FOOL||||||||||||\n")
			print("you cant beat the", card_to_def, "with the", card_to_def_with)

	# _cardsToDefend is empty; discard cards
	for card in _buffer:
		discard.append(card)

class Player:
	def __init__(self, name, hand, took=False):
		self.name = name
		self.hand = hand
		self.took = took # flag for if player just took

	def attack(self):
		# attack with any card
		attack_cards = selectCards(self.name, self.hand, "to attack with")
		self.removeCards(attack_cards)
		return attack_cards

	def prettyHand(self):
		r0 = r1 = r2 = r3 = r4 = r5 = ""
		self.hand = durakSort(self.hand)
		for card in self.hand:
			symbol = prettyPrintSuit(card.suit)
			if card.value == "10":
				valueTop = valueBottom = "10"
			else:
				valueTop = card.value[0] + " "
				valueBottom = " " + card.value[0]
			#r0 += " _______   "
			r1 += "|" + valueTop + "     | "
			r2 += "|       | "
			r3 += "|   " + symbol + "   | "
			r4 += "|       | "
			r5 += "|     " + valueBottom + "| "
			n = "\n"
			strCat = r0+n+r1+n+r2+n+r3+n+r4+n+r5
		return strCat

	def defend(self, hand):
		# remind player of their hand
		self.hand = durakSort(self.hand)
		print("Time to Defend", self.name, "your hand is:\n")
		printHand(self.hand, "\n")

		# select card to defend
		card_to_defend = selectCards(self.name, hand, "to defend (OR 'take' TO TAKE)")

		# check if user took
		if (card_to_defend == 'take'):
			return ('take', 'take')
		
		#select card to defend with
		strCat = "to defend the [" + str(card_to_defend[0]) + "] with (OR 'take' TO TAKE)"
		card_to_defend_with = selectCards(self.name,self.hand, strCat)
		
		# check if user took (again)
		if (card_to_defend_with == 'take'):
			return ('take', 'take')

		# return if user defended successfully
		return(card_to_defend, card_to_defend_with)
	
	def take(self, junk):
		for item in list(junk):
			self.hand.append(item)

	def addCards(self, cards_played):
		legal_attack_cards = []
		while(True):
			ac = selectCards(self.name, self.hand, "to add on (or 'done')")
			if (type(ac) != list and ((ac.lower() == 'done') or (ac == ''))):
				return []
			if (len(ac) > 0):
				listOfLegalValues = [x.value for x in cards_played]
				for card in ac:
					if card.value in listOfLegalValues:
						legal_attack_cards.append(card)
					else:
						print(" |!|!|!|!|!|!| FOOL you can't add [",card,"] |!|!|!|!|!|!|")
				if (len(legal_attack_cards) > 0):	
						self.removeCards(legal_attack_cards)
						return legal_attack_cards

	def removeCards(self, cards):
		self.hand = list(self.hand)

		# if cards is a single card
		if (type(cards) == pd.card.Card):
			self.hand.remove(cards)
		else:
			for card in cards:
				self.hand.remove(card)

	def printHand(self):
		for card in durakSort(self.hand):
			symbol = prettyPrintSuit(card.suit)
			print(symbol,card, symbol)

	def lengthHand(self):
		return len(self.hand)

	def justTook(self):
		return self.took 

	def set_justTook(self, took_):
		self.took = took_

def prettyPrintSuit(suit):
	l = {'Spades':   '♠','Diamonds': '♦','Hearts':   '♥','Clubs':    '♣', }
	return l[suit]

def printHand(hand, arg1='', arg2='', arg3=''):
	for card in durakSort(hand):
		symbol = prettyPrintSuit(card.suit)
		print(symbol,card,symbol)
	print(arg1, arg2, arg3)
		
def selectCards(name, stack, msg_append = ""):
	returnList = [] 

	# if one item in list return item
	if (type(stack) == pd.card.Card):
		return [stack]
	if (len(stack) == 1):
		return stack

	# print stuff
	message = "Select a card " + msg_append
	print(message, name)
	stack = durakSort(stack)
	for i in range(len(stack)):
		symbol = prettyPrintSuit(stack[i].suit)
		print(i, ":", symbol,stack[i],symbol)

	# collect user input
	user_input = input("Enter Selection (number, space seperated for multiple) here: ")

	# return user selection
	print("Excelent Choice! You selected:", end=' ')
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
