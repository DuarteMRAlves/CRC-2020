import math
import random as rand

class Player:

    def __init__(
        self, 
        initial_money: int,
        greediness: float,
        adaptiveness: float) -> None:
        '''
        initial_money: Initial money that the player has
        greediness: Number between 0 and 1. The closer to one the greedier
                    the player will behave, meaning it will offer less to the 
                    other player and will more easilly accept less fair offers
        adaptiveness: Number between 0 and 1. The closer to 1 the higher the
                      probability of the player to adapt when he encounters 
                      another player with a higher fitness (represents the beta value
                      in the probability of social learning)
        '''
        self.__money = initial_money
        self.__greediness = greediness
        self.__adaptiveness = adaptiveness

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        self.__money = value

    @property
    def greediness(self):
        return self.__greediness

    def propose_offer(self, ammount: float) -> bool:
        '''
        Returns the ammount to offer to another player given the initial
        received ammount
        '''
        return (1 - self.__greediness) * ammount / 2

    def accept_offer(self, ammount: float, total_ammount: float) -> bool:
        '''
        Returns true if the player wants to accept the offer and false
        otherwise
        '''
        ammount_percentage = ammount / total_ammount
        return ammount_percentage <= (1 - self.__greediness) / 2

    def adapt(self, other_player: 'Player') -> None:
        '''
        Adapt the player strategy according to the greediness
        If a player is greedier then he will start to follow
        the other player strategy. Otherwise he will not make
        many changes to its behaviour.
        self.__greediness functions as the learning rate parameter 
        in machine learning
        New greediness is an weighted average of the previous
        greediness with the other player's greediness
        '''
        fitness_delta = other_player.money - self.__money
        if self.__should_adapt(fitness_delta):
            greediness = self.__greediness
            self.__greediness = greediness * other_player.greediness + \
                                (1 - greediness) * greediness
    
    def __should_adapt(self, fitness: float) -> bool:
        '''
        Sigmoid function to compute adapt propability
        '''
        return fitness > 0
