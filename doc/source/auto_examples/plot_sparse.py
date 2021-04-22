"""
Which way did they go?
======================
"""

##############################
# The undirected graph
# --------------------
# Use the following commands to first plot the undirected graph
# of patient transfers.

from vizcovidfr.sparse import sparse
sparse.sparse_graph(directed=False)

##############################
# Do you remember which way did the patient go?
# You can figure it out with the next part
#
# The directed graph
# ------------------
# Use the following commands to plot the directed graph
# of patient transfers.

sparse.sparse_graph(directed=True)
