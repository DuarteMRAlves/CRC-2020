import csv
import networkx as nk

FILE_NAME = 'requirements.csv'

G = nk.DiGraph()
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
print(f'# packages with multiple versions: {len(mult_versions)}')
