import collections
import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

FILE_NAME = 'requirements.csv'

G = nx.DiGraph()
edges = set()

versions = {}
mult_versions = set()

with open(FILE_NAME, 'r') as fp:
    csv_stream = csv.reader(fp, delimiter=',')
    for row in csv_stream:
        # Unpack row for easy processing
        package, requirement, package_name, package_version = row

        if package_name in versions:
            if package_version != versions[package_name]:
                mult_versions.add(package_name)
        else:
            versions[package_name] = package_version
        
        if package_name and requirement:
            G.add_edge(package_name, requirement)
            edges.add((package_name, requirement))
        elif package_name:
            G.add_node(package_name)
        elif requirement:
            G.add_node(requirement)

print(f'# Nodes: {G.order()}, # Edges: {G.size()}')
print(f'# Packages with multiple versions: {len(mult_versions)}')
print(f'Average degree {G.size()/G.order()}')

# In Degrees

in_degrees = [degree for node, degree in G.in_degree()]
in_degree_count = collections.Counter(in_degrees)

in_pairs = sorted([(degree, count / G.order()) for degree, count in in_degree_count.items()], 
                  key=lambda x: x[0])

unique_in_degrees = [el[0] for el in in_pairs]
in_frequencies = [el[1] for el in in_pairs]

reversed_in_degrees = reversed(unique_in_degrees)
reversed_in_frequencies = reversed(in_frequencies)

cum_in_frequencies = np.cumsum(list(reversed_in_frequencies))
average_in_degree = np.sum(in_degrees) / G.order()

print(f"Avergae in degree: {average_in_degree}")

# Out Degrees

out_degrees = [degree for node, degree in G.out_degree()]
out_degree_count = collections.Counter(out_degrees)

out_pairs = sorted([(degree, count / G.order()) for degree, count in out_degree_count.items()], 
                   key=lambda x: x[0])

unique_out_degrees = [el[0] for el in out_pairs]
out_frequencies = [el[1] for el in out_pairs]

reversed_out_degrees = reversed(unique_out_degrees)
reversed_out_frequencies = reversed(out_frequencies)

cum_out_frequencies = np.cumsum(list(reversed_out_frequencies))

average_out_degree = np.sum(out_degrees) / G.order()

print(f"Avergae out degree: {average_out_degree}")

# Draw

fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2)

ax11.scatter(unique_out_degrees, out_frequencies)
ax11.set_title("Out Degree Distribution")
ax11.set_ylabel("Frequency")
ax11.set_xlabel("Degree")
ax11.set_xscale('log')
ax11.set_xticks([10e-2, 10e-1, 10e0, 10e1, 10e2])
ax11.set_yscale('log')
ax11.set_yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1])

ax12.scatter(list(reversed_out_degrees), cum_out_frequencies)
ax12.set_title("Out Degree Cumulative Distribution")
ax12.set_ylabel("Frequency")
ax12.set_xlabel("Degree")
ax12.set_xscale('log')
ax12.set_xticks([10e-2, 10e-1, 10e0, 10e1, 10e2])
ax12.set_yscale('log')
ax12.set_yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1])

ax21.scatter(unique_in_degrees, in_frequencies)
ax21.set_title("In Degree Distribution")
ax21.set_ylabel("Frequency")
ax21.set_xlabel("Degree")
ax21.set_xscale('log')
ax21.set_xticks([10e-2, 10e-1, 10e0, 10e1, 10e2])
ax21.set_yscale('log')
ax21.set_yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1])

ax22.scatter(list(reversed_in_degrees), cum_in_frequencies)
ax22.set_title("In Degree Cumulative Distribution")
ax22.set_ylabel("Frequency")
ax22.set_xlabel("Degree")
ax22.set_xscale('log')
ax22.set_xticks([10e-2, 10e-1, 10e0, 10e1, 10e2])
ax22.set_yscale('log')
ax22.set_yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1])

plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, 
                    hspace=0.5, wspace=0.3)

#plt.show()


# Clustering coeficient

print(f'Clustering Coefficient: {nx.average_clustering(G)}')
clustering_coefficients = list(sorted(nx.clustering(G).items(), key=lambda x: -x[1]))
print(f'10 Higher Clustering Coefficents: {clustering_coefficients[:10]}')

print(f'# Strongly Connected Components: {nx.number_strongly_connected_components(G)}')
print(f'Biggest Strongly Connected Component: {len(max(nx.strongly_connected_components(G), key=len))}')

print('Average Path Length Not Defined')

# Degree Centrality

reversed_in_degrees = list(sorted(G.in_degree(), key=lambda x: -x[1]))
print(f'10 Higher In Degree: {reversed_in_degrees[:10]}')
networkx = next(filter(lambda x: x[0] == 'networkx', reversed_in_degrees))
print(f'In Degree for Networkx: {networkx}')

reversed_out_degrees = list(sorted(G.out_degree(), key=lambda x: -x[1]))
print(f'10 Higher Out Degree: {reversed_out_degrees[:10]}')
networkx = next(filter(lambda x: x[0] == 'networkx', reversed_out_degrees))
print(f'Out Degree for Networkx: {networkx}')
