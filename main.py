import pydealer as pd
import logging
import inspect
from pydealer import Card
from termcolor import colored

# globals
kozer = 'Diamonds'
s = " ////////// "
b  = " \\\\\\\\\\\\\\\\\\\\ "
x =" |!|!|!|!|!|!| "  
g_MAXCARDSDISPLAY = 12 # max num cards pretty printed on screen

# create and configure logger
logging.basicConfig(filename = "./logs/testLog",level = logging.DEBUG, filemode = 'w')
logger = logging.getLogger()

def main():
	joshWins = nuaWins = mannyWins = adamWins = 0
	logger.info("Hello hello, top of main()")
	for i in range(1):
		# create players, deck, discard
		logger.info("BOUTTA INIT GAME")
		josh, adam, manny, nua, kozer, deck, discard = initGame()

		# play a game, returns 'winner'
		winner = playAGame(josh, nua, manny, adam, kozer, deck, discard)
		print(colored("Game Over! Winner was " + winner.name))
		logger.info("\ngame over! Winner was " + winner.name + "\n")
		logger.info("\t after game " + str(i) +" , discard = " + str(prettyShort(discard)))
		if (winner == josh):
			joshWins += 1
		if (winner == nua):
			nuaWins += 1
		if (winner == manny):
			joshWins += 1
		if (winner == adam):
			nuaWins += 1

	print(colored("EVERYTHING OVER, SCORES ARE:", 'yellow'))
	print(colored("\tJOSH (1st attack): " + str(joshWins), 'yellow'))
	print(colored("\tNUA (1st defence): " + str(nuaWins), 'yellow'))
	print(colored("\tMANNY (1st attack): " + str(joshWins), 'yellow'))
	print(colored("\tADAM (1st defence): " + str(nuaWins), 'yellow'))

def playAGame(attacker, defender, player3, player4, kozer, deck, discard=[]):
	players = [[attacker, 1], [defender, 2], [player3, 3], [player4, 4]]

	print(colored("welcome! kozer = " + kozer))
	logger.info("\n" + s + "Top of playAGame, kozer=" + kozer + b + "\n", 'yellow')
	logger.info("discard = " + str(prettyShort(discard)))
	while(True):
		# plays a round, changes everyones hand + discard accordingly. returns winner if there is one
		roundInfo = playARound(players[0], players[1], players[2], player4, kozer, discard, deck)
		if roundInfo[0] != None:
			return roundInfo[0]

		actualDefender = roundInfo[1]

		# round returns state
		# roundInfo = [winner, defender]
		# roundInfo = [None, defender]
		if actualDefender.justTook():
			attacker = players[players[actualDefender] + 1]
			

		# take, changes everyones hands and deck accordingly
		logger.info("right before take, len(deck) = " + str(len(deck)))
		logger.info("deck = " + str(prettyShort(deck)))
		take((attacker, defender, player3, player4), deck)
		
		# See if someone won, and return winner
		cw = checkWinner([attacker, defender, player3, player4], len(deck))
		if cw != None:
			return cw

		# some messages
		message_1(attacker, defender, deck, discard)

		# switch places
		if not (defender.justTook()):
			temp = attacker
			attacker = defender
			defender = temp
		else:
			print(colored("~~~~~~ Defender took, so attacker attacks again ~~~~~~"))
			logger.info("~~~ Defender took, so attacker ("+attacker.name+") attacks ~~~")
			defender.set_justTook(False)

def initGame():
	# initialize stuff
	deck = createDurakDeck()
	logger.info("inside initGame, len(deck) = " + str(len(deck)))
	discard = []
	hands = []
	deck.shuffle()
	#kozer = 'Diamonds' #declared globally 

	# deal 2 hands
	for i in range(4):
	    hands.append(list(deck.deal(6)))

	logger.info("inside initGame (AFTER DEAL), len(deck) = " + str(len(deck)))
	# assign a player to each hand
	josh = dumbAI("josh", hands[0])
	nua = dumbAI("nua", hands[1])
	manny = dumbAI("manny", hands[2])
	manny = dumbAI("adam", hands[3])

	logger.info("inside initGame RIGHT BEFORE RETURN, len(deck) = " + str(len(deck)))
	return josh, nua, kozer, deck, discard

def take(players, deck, sizeFullHand=6):
	for player in players:
		while( len(player.hand) < sizeFullHand):
			if (len(deck) > 0):
				player.take(deck.deal(1))
			else:
				logger.info("DECK IS NOW EMPTY (inside take())")
				print(colored("DECK IS NOW EMPTY"))
				return

def playARound(attacker, defender, kozer_suit, discard, deck):
	''' This function is hella long. This is where most of the magic happens'''

	# log relevant info
	log_relevant_round_info(attacker, defender, deck)

	# internal variables
	_buffer = [] 							# covered pairs on table. Will eventually be taken or discarded 
	cardCount = 0 							# how many cards have been played
	MAXCARDS = min(6, len(defender.hand)) 	# max cards that can be played

	# attacker attacks with any card (or multiple of same value)
	print(colored("\n" + s + attacker.name + s + "ATTACK" + s + defender.name + s, 'yellow'))
	print(colored(str(MAXCARDS) + "cards can be played",'yellow'))
	print(colored(attacker.name + "- select card to attack with:"))
	_cardsToDefend = attacker.attack(MAXCARDS)
	# See if attacker just got rid of all cards and won
	cw = checkWinner(attacker, defender, len(deck))
	if cw != None:
		return cw
	
	logger.info("attacker (" + attacker.name + ") attacks with: " + prettyShort(_cardsToDefend))
	cardCount += len(_cardsToDefend)
	logger.info("cardCount = " + str(cardCount))

	# defender defends until no more cards to defend TODO: (or 6 total)
	print(colored("\n" + s + defender.name + s + "DEFEND" + s + attacker.name + s, 'cyan'))
	while(len(_cardsToDefend) > 0):
		# defender selects 'take', or card_to_defend and card_to_defend_with 
		card_to_def, card_to_def_with = defender.defend(_cardsToDefend)

		# Check if cards actually beats
		if (card_to_def == 'take'):
			defender.set_justTook(True)
		if (defender.justTook()) or checkBeats(card_to_def, card_to_def_with, kozer_suit):
			if not (defender.justTook()): # if checkBeats() but dont run checkBeats twice
				# print success message
				print_and_log_success_message(defender, card_to_def, card_to_def_with)

				# remove cards from hand and _cardsToDefend and add to buffer
				defender.removeCards(card_to_def_with)
				_cardsToDefend.remove(card_to_def)
				_buffer.append(card_to_def)
				_buffer.append(card_to_def_with)

			# attacker optionally add cards
			print(colored("DEFENDER("+defender.name+") CARD COUNT:"+str(len(defender.hand)),'yellow'))
			print(colored("NUM CARDS CAN BE ADDED: " + str(MAXCARDS - cardCount), 'yellow'))
			cardsToAdd = attacker.addCards(_buffer + _cardsToDefend, MAXCARDS-cardCount, len(_buffer))
			logger.info("attacker (" + attacker.name + ") adds: " + prettyShort(cardsToAdd))
			print(colored("attacker (" + attacker.name + ") adds: " + prettyShort(cardsToAdd) ,'yellow'))
			# See if someone won, and return winner
			cw = checkWinner(attacker, defender, len(deck))
			if cw != None:
				return cw
			for card in cardsToAdd:
				_cardsToDefend.append(card)

			# check if defender took
			if (defender.justTook()):
				defender.take(_buffer)
				defender.take(_cardsToDefend)
				_cardsToDefend = [] #Is this line necessary?
				return 
					
		else: # else for 'if (checkBeats):'
			logger.info(x + "Defenders' selection is invalid, " + "["  + \
			prettyShort(card_to_def_with) + "] doesn't beat the [" + prettyShort(card_to_def) + "] " + x, 'red')
			print(colored(x + "FOOL YOU CANT BEAT THE [" + str(card_to_def) + "] WITH THE " \
				+ "[" + str(card_to_def_with) + "]" + x,'red'))

	# _cardsToDefend is empty; discard cards
	for card in _buffer:
		discard.append(card)

class Player:
	def __init__(self, name, hand, took=False):
		self.name = name
		self.hand = hand
		self.took = took # flag for if player just took

	def attack(self, num): #num = num(cards) allowed to be played
		# attack with any card
		while(True):
			attack_cards = selectCards(self.name, self.hand, "to attack with")
			if len(attack_cards) <= num:
				self.removeCards(attack_cards)
				return attack_cards
			print(colored(x + "yo you can only add " + str(num) + " cards" + x,'red'))

	def prettyHand(self, short=False):
		r0 = r1 = r2 = r3 = r4 = r5 = strCat = ""
		self.hand = durakSort(self.hand)

		# if hand is too long dont prettyPrint
		if ((len(self.hand) > g_MAXCARDSDISPLAY) or (short)):
			return prettyShort(self.hand)

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
		print(colored("Time to Defend " + self.name + " your hand is:\n " + self.prettyHand()))

		# select card to defend
		if (len(hand) > 1):
			card_to_defend = selectCards(self.name, hand, "to defend (OR 'take' TO TAKE)")
		else:
			card_to_defend = hand

		# check if user took (during first selection)
		if (card_to_defend == 'take'):
			return ('take', 'take')
		
		#select card to defend with
		sym = prettyPrintSuit(card_to_defend[0].suit)
		strCat = "to defend the [" + sym + " " + str(card_to_defend[0]) + " " + sym + "] with (OR 'take' TO TAKE)"
		card_to_defend_with = selectCards(self.name,self.hand, strCat)
		
		# check if user took (during second selection)
		if (card_to_defend_with == 'take'):
			return ('take', 'take')

		# bug fixing
		if type(card_to_defend) == list:
			card_to_defend = card_to_defend[0]
		card_to_defend_with = card_to_defend_with[0]

		# return if user defended successfully
		return(card_to_defend, card_to_defend_with)
	
	def take(self, junk):
		for item in list(junk):
			logger.info(self.name+"BOUTTA TAKE the "+str(prettyShort(item)) + "hand: " + str(prettyShort(self.hand)))
			self.hand.append(item)
			logger.info(self.name+"JUST TOOK the " + str(prettyShort(item)) + "hand: " + str(prettyShort(self.hand)))

	def addCards(self, cards_played, allowed, numCardsInBuffer):
		# internal variables
		legal_attack_cards = [] 	# holds (legal) cards to be added
		have_legal_cards = False	# does player have cards they can add
		listOfLegalValues = list(set(x.value for x in cards_played)) # list of legal values for adding
		print("LEGAL CARDS FOR ADDING:", listOfLegalValues)

		# check if player has atleast one card which can be legally added
		for card in self.hand:
			if card.value in listOfLegalValues:
				have_legal_cards = True

		# return empty if player cant add anything
		if not have_legal_cards:
			print(colored("No Cards can be added by attacker, moving on...",'yellow'))
			logger.info("No cards can be added by attacker, moving on...")
			return []
			
		while(True): # TODO
			ac = selectCards(self.name, self.hand, "to add on (or 'done')")
			if (type(ac) != list and ((ac.lower() == 'done') or (ac == ''))):
				return []
			if (len(ac) > allowed):
				print(colored(x + "FOOL you can only add " + str(allowed) + " cards" + x, 'red'))
			if (len(ac) > 0): #TODO check if this can be replaced with 'else:'
				for card in ac:
					if type(card) == pd.card.Card and (card.value in listOfLegalValues):
						legal_attack_cards.append(card)
					else:
						print(colored(x + "FOOL you can't add [" + str(card) + "]" + x, 'red'))
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
			print(colored(symbol,card, symbol))

	def justTook(self):
		return self.took 

	def set_justTook(self, took_):
		self.took = took_

class dumbAI(Player):
	def attack(self, num):
		# attacks with the lowest card
		atk_card = durakSort(self.hand)[0]
		self.removeCards(atk_card)
		return [atk_card]

	def addCards(self, cards_played, allowed, numCardsInBuffer): #dumbAI
		length = numCardsInBuffer/2
		MAX = Card(value='Jack', suit='Diamonds')
		add_cards = []
		have_legal_cards = False
		listOfLegalValues = list(set(x.value for x in cards_played))
		print("LEGAL CARDS FOR ADDING:", listOfLegalValues)
		logger.info("LEGAL CARDS FOR ADDING: " + str(listOfLegalValues))
		
		for card in self.hand:
			if card.value in listOfLegalValues:
				if card.suit != kozer or (length > 2 and card.lt(MAX)):
					if len(add_cards) < allowed:
						add_cards.append(card)
		
		if (len(add_cards) > 0):
			self.removeCards(add_cards)
			logger.info("inside dumbAI::addCards (" + self.name + ") hand is now: " + str(prettyShort(self.hand)))
			return add_cards
		else:
			print(colored("No Cards can be added by attacker, moving on...",'yellow'))
			logger.info("No cards can be added by attacker, moving on...")
			return []

	def defend(self, hand): #dumbAI

		# select card to defend
		if (len(hand) > 1):
			card_to_defend = selectLowestCard(hand)
		else:
			card_to_defend = hand[0]
	
		# check each card if it beats
		for card in durakSort(self.hand):
			logger.info("checking if " + str(prettyShort(card)) + " beats " + str(prettyShort(card_to_defend)))
			if checkBeats(card_to_defend, card, kozer):
				return (card_to_defend, card)
		print(colored("AI aint got nothing, forced to TAKE", 'red'))
		logger.info("Oh Bummer, I got nothing. Returning ('take', 'take')")
		return ('take', 'take')

def checkWinner(attacker, defender, deckLength):
	if ((deckLength == 0) and (len(attacker.hand) == 0)):
		logger.info("GAME OVER, winner was: " + attacker.name)
		return attacker

	if ((deckLength == 0) and (len(defender.hand) == 0)):
		logger.info("GAME OVER, winner was: " + defender.name)
		return defender
	return None

def prettyPrintSuit(suit):
	l = {'Spades':   '♠','Diamonds': '♦','Hearts':   '♥','Clubs':    '♣', }
	return l[suit]

def prettyShort(stack):
	strCat = "["
	if (type(stack) == pd.card.Card):
		stack = [stack]
	for card in stack:
		strCat += card.value + prettyPrintSuit(card.suit) + " "
	return str(strCat).rstrip() + "]"

def selectLowestCard(stack):
	return durakSort(stack)[0]

def selectCards(name, stack, msg_append = ""):
	while True:
		returnList = [] 

		# if one item in list return item
	#	if (type(stack) == pd.card.Card):
#			return [stack]
#		if (len(stack) == 1):
#			return stack

		# Create list_valid_entries
		list_valid_strings = ['done', 'take']	
		list_valid_entries = [str(x) for x in range(0, len(stack))]
		stack = durakSort(stack)

		# print stuff
		message = "Select a card " + msg_append
		print(colored(message + " " + name))
		for i in range(len(stack)):
			symbol = prettyPrintSuit(stack[i].suit)
			print(i, ":", symbol,stack[i],symbol)

		# collect user input
		user_input = input("Enter Selection (number, space seperated for multiple) here: ")
		print(colored("you entered " + user_input, 'yellow'))
			
		# return user selection
		for selection in user_input.split():
			if (user_input.lower() in list_valid_strings):
				print(colored("that WAS in the list of valid strings", 'yellow'))
				return user_input.lower()
			if (selection.strip() in list_valid_entries):
				returnList.append(stack[int(selection)])
			else:
				print(colored("ok that was an invalid entry *cough* NUA *cough*", 'red'))
				continue

		# TODO: Figure out if this if statement is necessary
		if (len(returnList) == 0):
			print(colored("Bruh none of what you just wrote was valid", 'red'))
			continue
		return returnList

def checkBeats(atkCard, defCard, kozer):
	if (atkCard.suit == defCard.suit):
		return atkCard.lt(defCard)
	else:
		return (defCard.suit == kozer) and (defCard.gt(atkCard) or atkCard.suit != kozer)

def durakSort(arr): # uses quicksort
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

def createDurakDeck():
	deck_ = pd.Deck()
	deck_.empty()
	deck_.add([Card(value='6', suit='Diamonds'), Card(value='6', suit='Clubs'), Card(value='6', suit='Hearts'), Card(value='6', suit='Spades'), Card(value='7', suit='Diamonds'), Card(value='7', suit='Clubs'), Card(value='7', suit='Hearts'), Card(value='7', suit='Spades'), Card(value='8', suit='Diamonds'), Card(value='8', suit='Clubs'), Card(value='8', suit='Hearts'), Card(value='8', suit='Spades'), Card(value='9', suit='Diamonds'), Card(value='9', suit='Clubs'), Card(value='9', suit='Hearts'), Card(value='9', suit='Spades'), Card(value='10', suit='Diamonds'), Card(value='10', suit='Clubs'), Card(value='10', suit='Hearts'), Card(value='10', suit='Spades'), Card(value='Jack', suit='Diamonds'), Card(value='Jack', suit='Clubs'), Card(value='Jack', suit='Hearts'), Card(value='Jack', suit='Spades'), Card(value='Queen', suit='Diamonds'), Card(value='Queen', suit='Clubs'), Card(value='Queen', suit='Hearts'), Card(value='Queen', suit='Spades'), Card(value='King', suit='Diamonds'), Card(value='King', suit='Clubs'), Card(value='King', suit='Hearts'), Card(value='King', suit='Spades'), Card(value='Ace', suit='Diamonds'), Card(value='Ace', suit='Clubs'), Card(value='Ace', suit='Hearts'), Card(value='Ace', suit='Spades')])
	return deck_
def print_and_log_success_message(defender, card_to_def, card_to_def_with):
	print(colored(s + defender.name + " succesfully defends the [" + str(card_to_def) \
	 + "] with the [" + str(card_to_def_with) + "]" + b, 'green'))
	logger.info(s + defender.name + " succesfully defends the [" + \
	prettyShort(card_to_def) + "] with the [" + prettyShort(card_to_def_with) + "]" + b)

def log_relevant_round_info(attacker, defender, deck):
	logger.info("------- Top of playARound() ----------")
	logger.info("\tattacker (" + attacker.name + ") Hand: " + str(prettyShort(durakSort(attacker.hand))))
	logger.info("\tdefender (" + defender.name + ") Hand: " + str(prettyShort(durakSort(defender.hand))))
	logger.info("len(deck): " + str(len(deck)))
	logger.info("deck = " + str(prettyShort(deck)))

def message_1(attacker, defender, deck, discard):
	print(colored("------ After Round -------- (msg_1)"))
	print(colored("\nlen(deck) is now: " + str(len(deck))))
	print(colored("discard = " + prettyShort(discard))) #TODO: make method shortPrettyPrint() or something 
	logger.info("\n\n------ After Round --------\n")
	logger.info(attacker.name + " hand is now: " + attacker.prettyHand(True))
	logger.info(defender.name + " hand is now: " + defender.prettyHand(True))
	logger.info("\nlen(deck) is now: " + str(len(deck)))
	logger.info("discard = " + prettyShort(discard)) 

if __name__ == "__main__":
	main()
