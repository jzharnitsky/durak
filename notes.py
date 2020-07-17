# list all legal moves from state

# curr action
	# [player] attack
		# kozer
		# cards in hand
		# all rounds history
			# cards in discard
			# num cards left in deck

	# [player] addCards
		# kozer
		# cards in hand
		# all rounds history
			# cards in discard
			# num cards left in deck
		# **cards on table**
			# face up cards
			# tuple(card covered, cardCoveredBy)
		
	# [player] defend
		# kozer
		# cards in hand
		# all rounds history
			# cards in discard
			# num cards left in deck
		# **cards on table**
			# face up cards (cardsToBeBeaten)
			# tuple(cardCovered, cardCoveredBy)
