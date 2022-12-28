import networkx as nx
import pandas as pd
import numpy as np
import re

# Import data.
edges = pd.read_csv('dataset/archive/edges.csv')
hero_network = pd.read_csv('dataset/archive/hero-network.csv')
nodes = pd.read_csv('dataset/archive/nodes.csv')

# Remove last space and "/" if present.
def remove_extra(row):
    return row.rstrip().rstrip('/')

hero_network['hero1'] = hero_network['hero1'].apply(remove_extra)
hero_network['hero2'] = hero_network['hero2'].apply(remove_extra)
edges['hero'] = edges['hero'].apply(remove_extra)
edges['comic'] = edges['comic'].apply(remove_extra)
nodes['node'] = nodes['node'].apply(remove_extra)

# Cut to max 20 characters hero's names.
edges['hero'] = edges['hero'].apply(lambda row: row[:20])
nodes['node'] = nodes['node'].apply(lambda row: row[:20])

# Remove row with same hero (self-loop).
hero_network.drop(hero_network[hero_network.hero1 == hero_network.hero2].index, inplace=True)
hero_network.reset_index(drop=True, inplace=True)



def first_graph(dataset):
    # Remake the dataframe sorting the names by row to check duplicates.
    dataset = pd.DataFrame(np.sort(dataset.values), columns=dataset.columns)

    # Store the edges weights in a sorted dictionary.
    edges_weight = dict(sorted(dict(round(1 / (dataset.hero1 + dataset.hero2).value_counts(), 5)).items()))

    # Drop duplicates.
    dataset.drop_duplicates(inplace=True)

    # Create "weight" column.
    dataset = dataset.sort_values(by=['hero1', 'hero2'])
    dataset['weight'] = edges_weight.values()

    # Generate the graph.
    graph = nx.from_pandas_edgelist(dataset, 'hero1', 'hero2', 'weight')

    return graph

def second_graph(nodes, edges):
    graph = nx.Graph()
    graph = nx.from_pandas_edgelist(edges, 'hero', 'comic')
    node_attr = nodes.apply(lambda row: (row.node, {'type': row.type}), axis=1)
    graph.add_nodes_from(node_attr)
    return graph

def top_N_heroes(N=-1):
    top_heroes = edges.groupby('hero').count().sort_values('comic', ascending=False)
    return list(top_heroes.iloc[:N].index)

def not_top_N_heroes(N=-1):
    top_heroes = edges.groupby('hero').count().sort_values('comic', ascending=False)
    return list(top_heroes.iloc[N:].index)

# Exported--------------------------
load_graph_1 = lambda: first_graph(hero_network)

load_graph_2 = lambda: second_graph(nodes, edges)

def top_N_filter(graph, N=-1):
    graph = graph.copy()
    graph.remove_nodes_from(not_top_N_heroes(N))
    return graph

