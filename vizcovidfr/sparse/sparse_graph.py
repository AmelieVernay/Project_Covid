import time
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.sparse import isspmatrix

from vizcovidfr.loads import load_datasets


def sparse_graph(directed=False):
    """
    Plot and return the graph of the transfer of patient with Covid-19,
    inside or outside France.

    :Notes:

    Try to first plot the undirected graph to see if you can guess the
    direction of the arrows, then check by calling the function with
    directed=True !

    Parameters
    ----------

    :param directed: whether we want the graph to be directed or not
    :type directed: bool, optional (default=False)

    Returns
    -------

    :return: plot the graph representation and return the graph object
    :rtype:
        networkx.classes.graph.Graph (if directed=False)
        networkx.classes.digraph.DiGraph (if directed=True)

    :Examples:

    >>> sparse_graph(directed=True)

    >>> sparse_graph(directed=False)
    """
    raw_transfer = load_datasets.Load_transfer().save_as_df()
    raw_transfer['region_arrivee'] = raw_transfer['region_arrivee'].replace(
                                                np.nan, 'outside France')
    # keep only relevent information
    transfer = raw_transfer[['region_depart',
                             'region_arrivee',
                             'nombre_patients_transferes']]
    # make a graph out of the transfer dataframe,
    if (directed):
        word = 'Directed'
        good_seed = 1133311  # it's a palindromic number!
        G = nx.from_pandas_edgelist(transfer, 'region_depart',
                                              'region_arrivee',
                                              'nombre_patients_transferes',
                                              create_using=nx.DiGraph())
    else:
        word = 'Undirected'
        good_seed = 41
        G = nx.from_pandas_edgelist(transfer, 'region_depart',
                                              'region_arrivee',
                                              'nombre_patients_transferes',
                                              create_using=nx.Graph())
    # ---------- plot graph ----------
    plt.figure(figsize=(13, 9))
    # set (good) seed for orientation purpose
    # draw graph
    nx.draw_networkx(G, with_labels=True,
                     pos=nx.spring_layout(G, seed=good_seed),
                     node_color='#d51e3999',
                     edge_color='#cc901699',
                     font_size=11)

    # extract edge 'weights' (i.e. number of transfered patients)
    labels = nx.get_edge_attributes(G, "nombre_patients_transferes")
    # add weights labels
    nx.draw_networkx_edge_labels(G,
                                 pos=nx.spring_layout(G, seed=good_seed),
                                 edge_labels=labels)
    # re-scale weights to avoid enormous edges
    lab_val = list(labels.values())
    scaled_lab_val = [element * 0.1 for element in lab_val]
    # draw egdes proportionately to weights
    if (directed):
        nx.draw_networkx_edges(G, pos=nx.spring_layout(G, seed=good_seed),
                               width=scaled_lab_val,
                               edge_color='#cc901699',
                               arrowstyle='->',
                               arrowsize=17)
    else:
        nx.draw_networkx_edges(G, pos=nx.spring_layout(G, seed=good_seed),
                               width=scaled_lab_val,
                               edge_color='#cc901699')

    plt.axis('off')
    plt.figtext(.5, .9, f'{word} graph of patient transfers',
                fontsize=17, ha='center')
    plt.show()
    return G


Ga = sparse_graph()

Ga


G["Bretagne"]["Grand Est"]["nombre_patients_transferes"]


# get adjacency matrix
A = nx.adjacency_matrix(G)
# is it sparse ? ...of course it is..it's an adjacency matrix!
print(isspmatrix(A))
# plot sparse adjacency matrix
plt.figure(figsize=(7, 7))
plt.spy(A, color='#971b8599')
plt.title('adjacency matrix of transfer graph')
# graph properties
G.number_of_edges()
G.number_of_nodes()
# percentage of matrix occupation
print((G.number_of_edges() / G.number_of_nodes()**2) * 100)
# 9.47%


B = A.todense()
print(isspmatrix(B))
A
B
start = time.time()
v = A.T
end = time.time()

print("Time to execute: {0:.5f} s.".format(end - start))


start = time.time()
v = B.T
end = time.time()

print("Time to execute: {0:.5f} s.".format(end - start))

# def an_addition(source, target):
#     # Check input
#     if type(source) == str or type(target) == str:
#         raise TypeError('We can only add numbers, not strings!')
#     if type(source) != type(target):
#         raise TypeError('We can only add numbers of the same type!')
#     # OK, go
#     return G[source][target]["nombre_patients_transferes"]
