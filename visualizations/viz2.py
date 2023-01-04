from collections import defaultdict
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from functions import top_N_filter, clean_comm

def centr_table(graph, metric, N):
    data = defaultdict(list)
    graph_tmp = top_N_filter(graph, N)
    for node in graph_tmp.nodes:
        data['node'].append(node)
        data['centrality'].append(functionality_2(graph, node, metric, N)[1])

    data['avg'] = sum(data['centrality'])/N

    return data

def functionality_2(graph, node, metric, N=6439):
    
    graph = top_N_filter(graph, N)

    metric = clean_comm(metric)
    result = eval(f'nx.{metric}(graph)[node]')
    return (node, result)

