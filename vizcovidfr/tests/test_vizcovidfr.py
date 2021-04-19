# ---------- requirements ----------
from scipy.sparse import isspmatrix

# local reqs
from vizcovidfr.maps import maps
from vizcovidfr.sparse import sparse


# ---------- maps ----------
def test_viz2Dmap():
    """
    Test viz2Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(maps.viz2Dmap()) != int)
    assert result


def test_viz3Dmap():
    """
    Test viz3Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(maps.viz3Dmap()) != int)
    assert result


def test_transfer_map():
    """
    Test transfer_map by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(maps.transfer_map()) != int)
    assert result


# ---------- sparse ----------
def test_sparse_graph():
    """
    Test sparse_graph. Call the function and check if the number of edges
    of the resulting graph is an integer.
    If not, an AssertionError will raise.
    """
    G = sparse_graph.sparse_graph(show=False)
    e = G.number_of_edges()
    result = (type(e) == int)
    assert result


def test_sparse_matrix():
    """
    Test sparse_matrix. Call the function and check if the resulting matrix
    is a sparse matrix.
    If not, an AssertionError will raise.
    """
    result = (isspmatrix(sparse_graph.sparse_matrix(show=False)))
    assert result
