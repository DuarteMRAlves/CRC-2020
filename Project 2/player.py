import random as rand

_MUTATION_RATE = 0.01

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
        accept_perc: float) -> None:

        assert initial_money >= 0
        assert 0 <= propose_perc <= 1
        assert 0 <= accept_perc <= 1

        self.__money = initial_money
        self.__propose_perc = propose_perc
        self.__accept_perc = accept_perc

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

    def child(self):
        '''
        Creates a new offspring for the player
        The child has the same characteristis with some small randomness
        '''
        player = Player(
            0,
            self.__propose_perc,
            self.__accept_perc)
        player.__mutate()
        return player

    def __mutate(self) -> None:
        delta1 = _MUTATION_RATE * rand.random() - _MUTATION_RATE / 2
        delta2 = _MUTATION_RATE * rand.random() - _MUTATION_RATE / 2
        #self.__propose_perc = np.clip(self.__propose_perc + delta1, 0, 1)
        #self.__accept_perc = np.clip(self.__accept_perc + delta2, 0, 1)
        self.__propose_perc = min(max(self.__propose_perc + delta1, 0), 1)
        self.__accept_perc = min(max(self.__accept_perc + delta2, 0), 1)
        assert 0 <= self.__propose_perc <= 1
        assert 0 <= self.__accept_perc <= 1
