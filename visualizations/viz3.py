import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from functions import top_N_filter
from random import sample


def visualization_3(graph2, h, h_1, h_n, N=6439):
    
    # Check if input value are good.
    if h_1 == 0:
        return

    path = functionality_3(graph2, h, h_1, h_n, N=N)

    # Handle exceptions: if there ids no path or not all heroes are in the graph.
    if path in [0, -1]:
        return 

    # Create the graph.
    G = nx.DiGraph()
    for i in range(len(path)-1):
        G.add_edge(path[i], path[i+1], weight = i)
    
    # Set type attribute to nodes.
    attr = {}
    for node in G.nodes():
        attr[node] = graph2.nodes[node]
    nx.set_node_attributes(G, attr)

    # Set different color for comics and heroes.
    c1, c2 = plt.cm.Set2(0), plt.cm.Set2(1) 
    node_color, color_comic, color_hero = [], c1, c2
    for node in G.nodes(data=True):
        if node[1]['type'] == 'comic':
            node_color.append(color_comic)
        elif node[1]['type'] == 'hero':
            node_color.append(color_hero)

    # Plot the graph.
    pos = {}
    pos.update( (n[0], (1, i*2)) for i, n in enumerate(G.nodes(data=True)) if n[1]['type'] == 'comic')
    pos.update( (n[0], (2, i*2)) for i, n in enumerate(G.nodes(data=True)) if n[1]['type'] == 'hero')

    nx.draw_networkx_nodes(G, pos, node_color=node_color, alpha=.7, node_size=450, node_shape='8')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1, alpha=.5, connectionstyle="arc3,rad=0.01")
    nx.draw_networkx_labels(G, pos, font_size=5)

    edge_labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5)

    handles = [plt.plot([], "o", color=c)[0] for c in [c1, c2]]
    plt.legend(handles, ['Comic', 'Hero'], ncol=2, loc="upper center", frameon=False, markerscale=2)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    
def functionality_3(graph2, h, h_1, h_n, N=6439):
    
    # Keep only the top N heroes.
    graph = top_N_filter(graph2, N, remove_isolates=True)

    # Check if all the heroes of the list are in the graph.
    seq = [h_1] + h + [h_n]
    if not all(i in graph.nodes() for i in seq):
        print("Not all the heroes are in the graph! Try to increase N")
        return -1

    # Find all the intermediate shortest paths.
    path = []
    for pos in range(len(seq)-1):
        source = seq[pos]
        target = seq[pos+1]
        try:
            new_step = nx.shortest_path(graph, source, target)

            # Check if the shortest path do not pass for nodes that appear later in list.
            if len(set(seq[pos+2:]).intersection(new_step)) == 0:
                path.extend(new_step[1:])
            else:

                # Find all the shortest paths and take the first that pass the condition.
                step_list = nx.all_shortest_paths(graph, source, target)
                for step in step_list:
                    if len(set(seq[pos+2:]).intersection(new_step)) == 0:
                        path.extend(step[1:])
                        break

        except:
            print("There is no such path")
            return 0
        
    # Take only the comics that the shortest path visits.
    comics = [step for step in path if graph.nodes[step]['type'] == 'comic']

    # Remove a comic if appears more than one time consecutively.
    comics = [comic for pos,comic in enumerate(comics[:-1]) if comic != comics[pos+1]] + [comics[-1]]

    print(f'The comics path from {h_1} to {h_n} is: {comics}')

    return [h_1] + path