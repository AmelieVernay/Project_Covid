import time
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.sparse import isspmatrix

from vizcovidfr.loads import load_datasets


def sparse_graph():
    """
    """
    raw_transfer = load_datasets.Load_transfer().save_as_df()
    raw_transfer['region_arrivee'] = raw_transfer['region_arrivee'].replace(
                                                np.nan, 'outside France')
    # keep only relevent informations
    transfer = raw_transfer[['region_depart',
                             'region_arrivee',
                             'nombre_patients_transferes']]
    # make a graph out of the transfer dataframe,
    G = nx.from_pandas_edgelist(transfer, 'region_depart',
                                          'region_arrivee',
                                          'nombre_patients_transferes')
    # ---------- plot graph ----------
    plt.figure(figsize=(14, 9))
    # set (good) seed for orientation purpose
    good_seed = 41
    # draw graph
    nx.draw_networkx(G, with_labels=True,
                     pos=nx.spring_layout(G, seed=good_seed),
                     node_color='#d51e3999',
                     edge_color='#cc901699')

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
    nx.draw_networkx_edges(G, pos=nx.spring_layout(G, seed=good_seed),
                           width=scaled_lab_val,
                           edge_color='#cc901699')

    plt.axis('off')
    plt.title('Graph of patient transfers')
    plt.show()
    return G


G = sparse_graph()


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
