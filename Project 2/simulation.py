import itertools
import arguments
import game
import matplotlib.pyplot as plt
import multiprocessing as mp
import networkx as nx
import numpy as np
import random as rand
import player as pl

NUM_ROWS = 10

args = arguments.Parser().arguments

num_players = args.a
num_simulations = args.s
num_rounds = args.i
punishment_ratio = args.n
punishment_probability = args.p
model = args.m

def grid_model(num_players):
    num_rows = NUM_ROWS
    num_columns = num_players // NUM_ROWS

    assert num_rows * num_columns == num_players

    grid_graph = nx.grid_2d_graph(num_rows, num_columns)

    generator = itertools.count()

    return nx.relabel_nodes(grid_graph, lambda _ : next(generator))


def minimal_model(num_players):
    assert num_players > 2
    players_connections = nx.Graph()
    players_connections.add_edge(0, 1)

    for i in range(2, num_players):
        edges = list(players_connections.edges)
        random_edge_idx = np.random.choice(len(edges), 1)[0]
        random_edge = edges[random_edge_idx]
        players_connections.add_edge(random_edge[0], i)
        players_connections.add_edge(random_edge[1], i)

    assert players_connections.order() == num_players

    return players_connections

def simulation(sim_number, players_connections):

    players = [ 
        pl.Player(0, rand.random(), rand.random()) 
        for _ in range(num_players) 
    ]
    players_idxs = np.arange(0, num_players, 1)
    gen = game.UltimatumGenerator(1, punishment_ratio, punishment_probability)

    mean_money_over_time = []
    upper_std_money_over_time = []
    lower_std_money_over_time = []
    propose_over_time = []
    accept_over_time = []

    for i in range(num_rounds):
        if i % 1000 == 0:
            print(f"{sim_number}: On round {i}")
        # Play game
        for _ in range(10):
            for pos1, pos2 in players_connections.edges():
                gen.play_round(players[pos1], players[pos2])
                gen.play_round(players[pos2], players[pos1])

        # Collect data
        money_values = [ p.money for p in players ]
        propose_percentages = [ p.propose_perc for p in players ]
        accept_percentages = [ p.accept_perc for p in players ]

        mean_money = np.mean(money_values)
        std_money = np.std(money_values)
        mean_money_over_time.append(mean_money)
        upper_std_money_over_time.append(mean_money + std_money)
        lower_std_money_over_time.append(mean_money - std_money)

        propose_over_time.append(np.mean(propose_percentages))
        accept_over_time.append(np.mean(accept_percentages))

        # Dont evolve the last population
        if i == num_rounds - 1:
            break
        # Evolve Population
        new_players = [None for _ in range(num_players)]

        for player_idx in players_connections.nodes():
            players_to_breed_idxs = list(players_connections.neighbors(player_idx))
            players_to_breed_idxs.append(player_idx)

            players_to_breed = [players[p].money for p in players_to_breed_idxs]

            fitness_values = np.array(players_to_breed)

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
    
    print(f"{sim_number}: Simulation Complete. Showing results")

    return (
        mean_money_over_time, 
        upper_std_money_over_time, 
        lower_std_money_over_time, 
        propose_over_time, 
        accept_over_time,
        players)

def draw_grid(
    players_connections, 
    players_propose, 
    players_accept,
    ax1,
    ax2):

    num_columns = players_connections.order() // NUM_ROWS

    pos = {x:(x % num_columns, x // num_columns) for x in players_connections.nodes()}

    nx.draw_networkx(
        players_connections, 
        pos=pos,
        ax=ax1, 
        node_color=np.mean(players_propose, axis=0), 
        vmin=0, 
        vmax=1, 
        cmap='coolwarm',
        with_labels=True)

    nx.draw_networkx(
        players_connections, 
        pos=pos,
        ax=ax2, 
        node_color=np.mean(players_accept, axis=0), 
        vmin=0, 
        vmax=1, 
        cmap='coolwarm',
        with_labels=True)
    

def draw_layout(
    players_connections, 
    players_propose, 
    players_accept,
    ax1,
    ax2,
    draw_fn):
    
    draw_fn(
        players_connections, 
        ax=ax1, 
        node_color=np.mean(players_propose, axis=0), 
        vmin=0, 
        vmax=1, 
        cmap='coolwarm',
        with_labels=True)

    draw_fn(
        players_connections, 
        ax=ax2, 
        node_color=np.mean(players_accept, axis=0), 
        vmin=0, 
        vmax=1, 
        cmap='coolwarm',
        with_labels=True)

def main():

    print(args)

    if model == 'complete':
        players_connections = nx.complete_graph(num_players)
    elif model == 'barabasi-albert':
        players_connections = nx.barabasi_albert_graph(num_players, 4)
    elif model == 'latice-1d':
        players_connections = nx.cycle_graph(num_players)
    elif model == 'latice-2d':
        players_connections = grid_model(num_players)
    elif model == 'minimal':
        players_connections = minimal_model(num_players)
    else:
        raise ValueError('Can not happen')

    mean_money = np.empty((num_simulations, num_rounds))
    upper_std_money = np.empty((num_simulations, num_rounds))
    lower_std_money = np.empty((num_simulations, num_rounds))
    mean_propose = np.empty((num_simulations, num_rounds))
    mean_accept = np.empty((num_simulations, num_rounds))

    players_propose = np.empty((num_simulations, num_players))
    players_accept = np.empty((num_simulations, num_players))

    with mp.Pool(num_simulations) as pool:

        TASKS = [(i, players_connections) for i in range(num_simulations)]
        results = [pool.apply_async(simulation, t) for t in TASKS]

        for i, r in enumerate(results):
            sim_mean_money, sim_upper_std_money, sim_lower_std_money, sim_propose, sim_accept, sim_players = r.get()
            mean_money[i] = sim_mean_money
            upper_std_money[i] = sim_upper_std_money
            lower_std_money[i] = sim_lower_std_money
            mean_propose[i] = sim_propose
            mean_accept[i] = sim_accept
            players_propose[i] = [p.propose_perc for p in sim_players]
            players_accept[i] = [p.accept_perc for p in sim_players]

    _, (ax1, ax2) = plt.subplots(1, 2)
    xticks = np.arange(0, num_rounds, 1)
    ax1.plot(xticks, np.mean(mean_money, axis=0), label='Mean')
    ax1.plot(xticks, np.mean(upper_std_money, axis=0), label='Mean + Std')
    ax1.plot(xticks, np.mean(lower_std_money, axis=0), label='Mean - Std')
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Money')
    ax1.legend()
    ax2.plot(xticks, np.mean(mean_propose, axis=0), label='Propose')
    ax2.plot(xticks, np.mean(mean_accept, axis=0), label='Accept')
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Mean Propose and Accept (%)')
    ax2.legend()
    ax2.set_ylim((0,1))
    ax2.set_yticks(np.arange(0, 1, 0.1))

    plt.subplots_adjust(wspace=0.3)

    # fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # (ax1, ax2) = axes

    # if model == 'complete':
    #     draw_layout(players_connections, players_propose, players_accept, ax1, ax2, nx.draw_circular)
    # elif model == 'barabasi-albert':
    #     draw_layout(players_connections, players_propose, players_accept, ax1, ax2, nx.draw_kamada_kawai)
    # elif model == 'latice-1d':
    #     draw_layout(players_connections, players_propose, players_accept, ax1, ax2, nx.draw_circular)
    # elif model == 'latice-2d':
    #     draw_grid(players_connections, players_propose, players_accept, ax1, ax2)
    # elif model == 'minimal':
    #     draw_layout(players_connections, players_propose, players_accept, ax1, ax2, nx.draw_kamada_kawai)
    # else:
    #     raise ValueError('Can not happen')

    # plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.1, hspace=0.1)
    # plt.axis('off')
    plt.show()

if __name__ == '__main__':
    main()
