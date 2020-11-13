import random as rand
import numpy as np

class Player:
    '''
    Class to model a single player
    Its fitness is represented by its money
    Its strategy is represented by its split percentage 
    accept percentage
    '''

    def __init__(
        self, 
        initial_money: int,
        propose_perc: float,
        accept_perc: float,
        adaptiveness: float) -> None:

        assert initial_money >= 0
        assert 0 <= propose_perc <= 1
        assert 0 <= accept_perc <= 1
        assert 0 <= adaptiveness <= 1

        self.__money = initial_money
        self.__propose_perc = propose_perc
        self.__accept_perc = accept_perc
        self.__adaptiveness = adaptiveness

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        self.__money = value

    @property
    def propose_perc(self):
        return self.__propose_perc

    @property
    def accept_perc(self):
        return self.__accept_perc

    def propose_offer(self, ammount: float) -> bool:
        '''
        Returns the ammount to offer to another player given the initial
        received ammount
        '''
        return self.__propose_perc * ammount

    def accept_offer(self, ammount: float, total_ammount: float) -> bool:
        '''
        Returns true if the player wants to accept the offer and false
        otherwise
        '''
        ammount_percentage = ammount / total_ammount
        return ammount_percentage >= self.__accept_perc

    def adapt(self, other_player: 'Player') -> None:
        '''
        Adapt the player strategy according to the other player
        '''
        fitness_delta = other_player.money - self.__money
        if self.__should_adapt(fitness_delta):
            self.__propose_perc = other_player.propose_perc
            self.__accept_perc = other_player.accept_perc
            # adaptiveness = self.__adaptiveness
            # self.__propose_perc = adaptiveness * other_player.propose_perc + \
            #                       (1 - adaptiveness) * self.__propose_perc

            # self.__accept_perc = adaptiveness * other_player.accept_perc + \
            #                      (1 - adaptiveness) * self.__accept_perc
            assert 0 <= self.__propose_perc <= 1
            assert 0 <= self.__accept_perc <= 1

    def mutate(self) -> None:
        # self.__propose_perc = rand.random()
        # self.__accept_perc = rand.random()
        delta1 = 0.1 * rand.random() - 0.05
        delta2 = 0.1 * rand.random() - 0.05
        self.__propose_perc = np.clip(self.__propose_perc + delta1, 0, 1)
        self.__accept_perc = np.clip(self.__accept_perc + delta2, 0, 1)
        assert 0 <= self.__propose_perc <= 1
        assert 0 <= self.__accept_perc <= 1

    def child(self):
        player = Player(
            0,
            self.__propose_perc,
            self.__accept_perc,
            self.__adaptiveness)
        if 0.1 < rand.random():
            player.mutate()
        return player
    
    def __should_adapt(self, fitness: float) -> bool:
        '''
        Sigmoid function to compute adapt propability
        '''
        return fitness > 0
