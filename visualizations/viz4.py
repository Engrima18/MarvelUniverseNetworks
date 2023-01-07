import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from functions import top_N_filter


def vis_4(graph, heroA, heroB, N=-1):
    
    # evaluate the min number of links to disconnect the graph
    min_cut, g1, g2 = functionality_4(graph, heroA , heroB, N)
    print(f'To disconnect the graph we have to remove {len(min_cut)} links')

    # original reduced graph
    small_graph = top_N_filter(graph, N)
   
    # plot the two networks before and after removing the edges
    fig, ax = plt.subplots(1, 2, figsize=(12,8))
    node_map1, edge_map1 = fit_colors(small_graph, heroA, heroB)

    layout = nx.random_layout(graph)
    nx.draw_networkx(small_graph, layout, with_labels=False,  node_color=node_map1, edge_color= edge_map1, ax=ax[0])

    # set the title
    ax[0].set_title("Original Network")

    # plot second graph
    small_graph.remove_edges_from(min_cut)

    node_map2, edge_map2 = fit_colors(small_graph, heroA, heroB)

    nx.draw_networkx(small_graph, layout, with_labels=False,  node_color=node_map2, edge_color= edge_map2, ax=ax[1])

    ax[1].set_title("Network without links")

    handles = [plt.plot([], marker="o", ls="", color=c)[0] for c in [plt.cm.Set2(0), plt.cm.Set2(2), plt.cm.Set2(3)]]
    labels = ['hero A', 'hero B', 'other heroes']
    plt.legend(handles, labels)

    
    plt.show()
    
    
def fit_colors(graph, hero1, hero2=None):
    '''Function for mapping colors when plotting the networks'''

    node_map = []
    for n in graph.nodes:
        if n == hero1: 
            node_map.append(plt.cm.Set2(0))
        elif n== hero2:
            node_map.append(plt.cm.Set2(2))
        else: 
            node_map.append(plt.cm.Set2(3))

    edge_map = []
    if hero2 != None:

        min_cut = list(nx.minimum_edge_cut(graph, s=hero1, t=hero2, flow_func=None))

        for e in graph.edges:
            if (e in min_cut) or (e[::-1] in min_cut):
                edge_map.append(plt.cm.Set2(1))
            else:
                edge_map.append(plt.cm.Set2(7))

    return (node_map, edge_map)


def functionality_4(graph, heroA, heroB, N=6439):
    
    # reducing the dimension of the original graph
    graph = top_N_filter(graph, N)

    # removing the min cut (max flow) between the two nodes
    min_cut = list(nx.minimum_edge_cut(graph, s=heroA, t=heroB, flow_func=None))
    graph.remove_edges_from(min_cut)

    # create two copies of the disconnected graph
    graphA = graph.copy()
    graphB = graph.copy()

    # evaluate the diwsconnected components (nodes)
    nodesA = nx.node_connected_component(graph, heroA)
    nodesB = nx.node_connected_component(graph, heroB)

    # remove nodes not owned by the connected component and create two separate graphs
    graphA.remove_nodes_from(nodesB)                                                                                                                                                    
    graphB.remove_nodes_from(nodesA)  
    
    return (min_cut, graphA, graphB)