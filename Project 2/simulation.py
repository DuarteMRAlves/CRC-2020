import copy as cp
import itertools
import game
import matplotlib.pyplot as plt
import numpy as np
import random as rand
import player as pl
import sys

NUM_ROUNDS = 10000
MUTATION_RATE = 0.01
ADAPTIVENESS = 0.5

def parse_args(argv):
    if len(argv) != 2:
        print("Wrong number of arguments: 1 Expected but received", len(argv))
        exit(1)
    return int(argv[1])

num_players = parse_args(sys.argv)
players = [ 
    pl.Player(0, rand.random(), rand.random(), ADAPTIVENESS) 
    for _ in range(num_players) 
]
players_idxs = np.arange(0, num_players, 1)
gen = game.UltimatumGenerator(10)

propose_over_time = []
child_propose_over_time = []
accept_over_time = []
child_accept_over_time = []

for i in range(NUM_ROUNDS):
    if i % 100 == 0:
        print(f"On round {i}")
    # Play game
    for j in range(num_players):
        for k in range(j + 1, num_players, 1):
            gen.play_round(players[j], players[k])

    # Collect data
    propose_percentages = [ p.propose_perc for p in players ]
    accept_percentages = [ p.accept_perc for p in players ]

    propose_over_time.append(np.mean(propose_percentages))
    accept_over_time.append(np.mean(accept_percentages))

    # Evolve Population
    fitness_values = [p.money for p in players]
    fitness_values /= np.sum(fitness_values)
    new_players_idxs = np.random.choice(players_idxs, size=num_players, p=fitness_values)

    new_players = [players[idx].child() for idx in new_players_idxs]

    players = new_players
    child_propose_over_time.append(np.mean([c.propose_perc for c in players]))
    child_accept_over_time.append(np.mean([c.accept_perc for c in players]))


print("Simulation Complete. Showing results")
players_money = [player.money for player in players]
_, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.hist(players_money, bins=50)
players_propose_perc = [player.propose_perc for player in players]
ax2.hist(players_propose_perc, bins=50)
players_accept_perc = [player.accept_perc for player in players]
ax3.hist(players_accept_perc, bins=50)

_, ax1 = plt.subplots(1, 1)
xticks = np.arange(0, NUM_ROUNDS, 1)
ax1.plot(xticks, propose_over_time)
ax1.plot(xticks, accept_over_time)
ax1.plot(xticks, child_propose_over_time)
ax1.plot(xticks, child_accept_over_time)

plt.show()
