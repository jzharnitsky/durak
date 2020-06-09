import pydealer
import pydealer.utils as utils
print(hand)
# TODOL

#create main method
# create game object
# create 4 hands
# deal each hand 6 cards, print all hands
def main():
    print("hello world")
    p1 = player("Josh")
    p2 = player("Nua")
    p3 = player("manny")
    p4 = player("adam")
    players = [p1, p2, p3, p4]
    game1 = game(players)
    game1.printHands() #theyre empty
    game1.init() # creates deck, deals cards
    game1.printHands() # prints cards in each hand

if __name__ == "__main__":
    main()

class Game:
    # Deck variable is local to game object
    deck = pydealer.Deck()
    def __init__(self, listOfPlayers):
        self.listOfPlayers = listOfPlayers

    def listPlayers (self):
        for player in listOfPlayers:
            print(player)

    def init(listOfPlayers):
        deck.shuffle()
        for player in listOfPlayers:
            player.hand = deck.deal(7)
            hand.sort()
            print("hand for player", player, "is", player.hand)
    def printHands(abc):
        print("print ahnds")

class player:
    def __init__(self, name):
        self.name = name
        self.hand = 


       





