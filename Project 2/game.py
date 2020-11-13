import player as pl

class UltimatumGenerator:

    def __init__(self, money_per_round) -> None:
        self.__money_per_round = money_per_round

    def play_round(self, donor: pl.Player, receiver: pl.Player):
        '''
        Plays a single round of the ultimatum game
        between the two players
        '''
        money_per_round = self.__money_per_round
        offer = donor.propose_offer(money_per_round)
        # If the receiver accept they both receive the money
        # Otherwise they stay the same
        if (receiver.accept_offer(offer, money_per_round)):
            donor.money += (money_per_round - offer)
            receiver.money += offer
            assert donor.money >= 0
            assert receiver.money >= 0
