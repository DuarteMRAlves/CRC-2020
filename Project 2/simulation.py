import game
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random as rand
import player as pl
import sys

NUM_ROUNDS = 20000
ADAPTIVENESS = 0.5

def parse_args(argv):
    if len(argv) != 2:
        print("Wrong number of arguments: 1 Expected but received", len(argv))
        exit(1)
    return int(argv[1])

num_players = parse_args(sys.argv)

players_connections = nx.barabasi_albert_graph(num_players, 4)
players = [ 
    pl.Player(0, rand.random(), rand.random(), ADAPTIVENESS) 
    for _ in range(num_players) 
]
players_idxs = np.arange(0, num_players, 1)
gen = game.UltimatumGenerator(10)

propose_over_time = []
accept_over_time = []

for i in range(NUM_ROUNDS):
    if i % 1000 == 0:
        print(f"On round {i}")
    # Play game
    for pos1, pos2 in players_connections.edges():
        gen.play_round(players[pos1], players[pos2])
        gen.play_round(players[pos2], players[pos1])

    # Collect data
    propose_percentages = [ p.propose_perc for p in players ]
    accept_percentages = [ p.accept_perc for p in players ]

    propose_over_time.append(np.mean(propose_percentages))
    accept_over_time.append(np.mean(accept_percentages))

    if i == NUM_ROUNDS - 1:
        break

    # Evolve Population
    new_players = [None for _ in range(num_players)]
    for player_idx in players_connections.nodes():
        players_to_breed_idxs = list(players_connections.neighbors(player_idx))
        players_to_breed_idxs.append(player_idx)
        fitness_values = np.array([players[p].money for p in players_to_breed_idxs])
        if np.all(fitness_values == 0):
            shape = (len(fitness_values),)
            uniform_probability = 1 / len(fitness_values)
            fitness_values = np.full(shape, uniform_probability)
        else:
            fitness_values /= np.sum(fitness_values)
        player_to_breed_idx = np.random.choice(
            players_to_breed_idxs, 
            size=1, 
            p=fitness_values)[0]
        new_players[player_idx] = players[player_to_breed_idx].child()

    players = new_players

print("Simulation Complete. Showing results")

_, ax1 = plt.subplots(1, 1)
xticks = np.arange(0, NUM_ROUNDS, 1)
ax1.plot(xticks, propose_over_time)
ax1.plot(xticks, accept_over_time)
ax1.set_ylim((0,1))


_, (ax1, ax2, ax3) = plt.subplots(1, 3)

money_values = [p.money for p in players]
nx.draw_networkx(
    players_connections, 
    ax=ax1, 
    node_color=money_values, 
    cmap='Blues', 
    with_labels=True)

propose_percentages = [p.propose_perc for p in players]
nx.draw_networkx(
    players_connections, 
    ax=ax2, 
    node_color=propose_percentages, 
    vmin=0, 
    vmax=0.5, 
    cmap='coolwarm',
    with_labels=True)

accept_percentages = [p.accept_perc for p in players]
nx.draw_networkx(
    players_connections, 
    ax=ax3, 
    node_color=accept_percentages, 
    vmin=0, 
    vmax=0.5, 
    cmap='coolwarm',
    with_labels=True)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.1, hspace=0.1)

plt.show()
