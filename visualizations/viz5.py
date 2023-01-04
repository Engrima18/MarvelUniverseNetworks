import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from functions import top_N_filter
plt.set_cmap('Set2')
set2_cmap = get_cmap('Set2')

def viz5(graph, hero1, hero2, N=-1):
    removed_edges, cc, same_community = func5(graph, hero1, hero2, N)
    graph = top_N_filter(graph, N)
    
    print('Minimum number of links to be removed:', removed_edges)
    max_len = max(map(len, cc))
    communities = {i:list(c) + (max_len - len(c)) * [pd.NA] for i,c in enumerate(cc)}
    
    print('\n\nCommunities:')
    display(pd.DataFrame(communities))
    
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    fig.set_size_inches((15,5))
    
    # Plot the original graph
    layout = nx.spring_layout(graph)
    ax1.set_title('Original Graph')
    nx.draw(graph, layout, ax=ax1, node_size=70)
    
    # Plot the graph showing the communities in the network
    color_dict = {n:np.nonzero(list(map(lambda c: n in c, cc)))[0][0] for n in graph.nodes}  
    color_map = list(color_dict.values())
    ax2.set_title('Communities')
    nx.draw(graph, layout, node_color=color_map, ax=ax2, node_size=70)
    
    # Plot the final graph and identify the community/communities of Hero_1 and Hero_2
    labels = {hero1:hero1, hero2:hero2}
    ax3.set_title('Heroes')
    nx.draw(graph,layout, node_color=color_map, ax=ax3, node_size=70)
    nx.draw_networkx_nodes(graph, layout, nodelist=labels.keys(), node_color=[color_dict[hero1], color_dict[hero2]], node_size=150, edgecolors='r')
    nx.draw_networkx_labels(graph,layout,labels,font_size=10,font_color='r', ax=ax3)
    
    plt.show()
    
    
def func5(graph, hero1, hero2, N=-1, k=2):
    '''K: number of comunities'''
    graph = top_N_filter(graph, N)
    
    cc = nx.number_connected_components(graph)
    removed_edges = 0
    while cc < k:
        edges_to_remove = most_ebc(graph)
        graph.remove_edges_from(edges_to_remove)
        if cc == 1:
            removed_edges += len(edges_to_remove)
        cc = nx.number_connected_components(graph)
        
    cc = list(nx.connected_components(graph))
    
    same_community = any([hero1 in community and hero2 in community for community in cc])
        
    return removed_edges, cc, same_community
    
def most_ebc(graph):
    '''Selects all edges which have maximum ebc'''
    ebc = nx.edge_betweenness_centrality(graph)
    M = max(ebc.values())
    edges = list(filter(lambda a: ebc[a] == M, ebc.keys()))
    return edges