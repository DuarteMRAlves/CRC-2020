import argparse

class Parser:

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        
        # Num of players
        parser.add_argument(
            '-a', 
            type=int, 
            default=50, 
            help='Number of agents in the simulation')

        # Num of simulations
        parser.add_argument(
            '-s', 
            type=int, 
            default=10, 
            help='Number of simulations to take averages')
        
        # Num of rounds
        parser.add_argument(
            '-i', 
            type=int, 
            default=1000, 
            help='Number of iterations in the simulation')

        # Punishment ratio
        parser.add_argument(
            '-n', 
            type=float, 
            default=0.0, 
            help='Punishment percentage')

        # Punishment probability
        parser.add_argument(
            '-p', 
            type=float, 
            default=0.0, 
            help='Punishment probability')
        
        # Model
        parser.add_argument(
            '-m', 
            choices=('complete', 'minimal', 'barabasi-albert', 'latice-1d', 'latice-2d'), 
            default='complete', 
            help='Type of graph to generate the connections between agents')

        self.__arguments = parser.parse_args()

    @property
    def arguments(self):
        return self.__arguments
