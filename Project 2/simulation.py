import game
import matplotlib.pyplot as plt
import numpy as np
import random as rand
import player as pl
import sys


ADAPTIVENESS = 0.5
NUM_ITERATIONS = 10000000

def parse_args(argv):
    if len(argv) != 2:
        print("Wrong number of arguments: 1 Expected but received", len(argv))
        exit(1)
    return int(argv[1])

num_players = parse_args(sys.argv)
players = [ pl.Player(0, rand.random(), ADAPTIVENESS) for _ in range(num_players) ]
gen = game.UltimatumGenerator(1000)

for i in range(NUM_ITERATIONS):
    if i % 10000 == 0:
        print(f"On iteration {i}")
    donor, receiver = rand.choices(players, k=2)
    gen.play_round(donor, receiver)

print("Simulation Complete. Showing results")
players_money = [player.money for player in players]
_, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(players_money, bins=50)
players_greediness = [player.greediness for player in players]
ax2.hist(players_greediness, bins=50)
plt.show()
