class game([player1, player2…]):
    # Setup (shuffle  + deal)

    # playARound (state)
        # attackingPlayer
        


class player(name, strategy aka algorithm)
    # all methods overwritten by strategy
    this.name = name
    this.status = attackingPlayer
    Attack()
    Transfer()
    Defend()
    Throw/add()
    Take()

class strategy()
 '''strategy consists of 4 submethods'''
 # strategy for when 'state' dicatates your status = attacking player
    def Attack():
        playLowestCard
 # strategy for when 'state' dicatates your status = defensive player
 # strategy for when 'state' dicatates your status = attackingPartner player
 # strategy for when 'state' dicatates your status = defendingPartner player


class state(data about whos attacking whos defending etc)
    # attacking player = josh
        Attack = enabled
        Defend = disabled
        .....
    # defending player = nua
        defend = enabled  # after defending transfer = disabled
        attack = disabled
        transfer = enabled 
    # attacking partner = manny
    # defending partner = adam ... etc..

main()
    PLayer player1 = player(strategy = aggresive)
    PLayer player2 = player(strategy = random)
    PLayer player3 = player(strategy = passive)
    game game1 = new game(player1, player2, player3)
    for i in range(100):
        game.play()
        record_results

