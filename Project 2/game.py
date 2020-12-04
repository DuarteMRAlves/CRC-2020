import player as pl
import numpy.random as np_rand

class UltimatumGenerator:

    def __init__(
        self, 
        money_per_round, 
        punishment_ratio,
        punishment_probability) -> None:

        self.__money_per_round = money_per_round
        self.__punishment_ratio = punishment_ratio
        self.__punishment_probability = punishment_probability

    def play_round(self, donor: pl.Player, receiver: pl.Player):
        '''
        Plays a single round of the ultimatum game
        between the two players
        '''
        money_per_round = self.__money_per_round
        offer = donor.propose_offer(money_per_round)
        # If the receiver accept they both receive the money
        # Otherwise they may receive punishment
        if (receiver.accept_offer(offer, money_per_round)):
            donor.money += (money_per_round - offer)
            receiver.money += offer
            assert donor.money >= 0
            assert receiver.money >= 0
        else:
            # With some probability the donor is punished for the offer
            if np_rand.random() < self.__punishment_probability:
                donor.money = max(donor.money - self.__punishment_ratio * money_per_round, 0)
            assert donor.money >= 0
            assert receiver.money >= 0
