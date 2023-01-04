import networkx as nx
import pandas as pd
from scipy import stats
from collections import Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from functions import top_N_filter
plt.set_cmap('Set2')
set2_cmap = get_cmap('Set2')

def viz1(graph, type, N=-1):
    node_number, collab, density, pmf, avg, hubs, is_dense = func1(graph, type, N)
    
    # print table
    print( '| Number of nodes | Density | Average degree | Is dense |')
    print( '|-----------------|---------|----------------|----------|')
    print(f'| {node_number:15} | {round(density, 3):7} | {round(avg, 3):14} | {"True" if is_dense else "False":8} |')
    
    display(pd.DataFrame(hubs, columns=['Hubs']))
    
    # A plot depicting the number of collaborations of each hero
    c = pd.DataFrame.from_dict(collab, orient='index').sort_values(by=0, ascending=False)
    plt.bar(x = c.index, height = c[0], color=set2_cmap(0))
    if type == 2:
        plt.title('# of heroes per comic')
    elif type==1:
        plt.title('# of collaborations per hero')
    if len(c) > 10:
        plt.xticks([])
    plt.show()
    
    # A plot depicting the degree distribution of the network
    xk = range(*pmf.support())
    plt.title(f'Graph {type} degree distribution')
    plt.vlines(xk, 0, pmf.pmf(xk), lw=1)
    plt.show()
    
    
def func1(graph, type, N=-1):
    graph = top_N_filter(graph, N)
    
    node_number = len(graph)
    if type==1:
        collab = dict(graph.degree)
    elif type==2:
        collab = dict(filter(lambda k: graph.nodes[k[0]]['type'] == 'comic', dict(graph.degree).items()))
    
    density = nx.density(graph)
    
    degree_count = Counter(dict(graph.degree).values())
    probs = np.array(list(degree_count.values()))/sum(degree_count.values())
    values = np.array(list(degree_count.keys()))
    pmf = stats.rv_discrete(name='degree', values=(values, probs))
    avg = pmf.mean()
    
    p95 = pmf.ppf(.95)
    hubs = [n for n,v in graph.degree if v >= p95]
    
    is_dense = density > 0.05
    
    return node_number, collab, density, pmf, avg, hubs, is_dense