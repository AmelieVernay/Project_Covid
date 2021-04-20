
# ---------- requirements ----------
from scipy.sparse import isspmatrix

# local reqs
from vizcovidfr.maps import maps
from vizcovidfr.maps import vacmaps
from vizcovidfr.sparse import sparse
from vizcovidfr.regression import regression
from vizcovidfr.line_charts import line_charts


# ---------- maps ----------
def test_viz2Dmap():
    """
    Test viz2Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(maps.viz2Dmap(file_path='')) != int)
    assert result


def test_viz3Dmap():
    """
    Test viz3Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(maps.viz3Dmap(file_path='')) != int)
    assert result


def test_transfer_map():
    """
    Test transfer_map by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(maps.transfer_map(file_path='')) != int)
    assert result

def test_vacmap():
    """
    Test vacmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    """
    result = (type(vacmaps.vacmap(file_path='')) != int)
    assert result


# ---------- sparse ----------
def test_sparse_graph():
    """
    Test sparse_graph. Call the function and check if the number of edges
    of the resulting graph is an integer.
    If not, an AssertionError will raise.
    """
    G = sparse.sparse_graph(show=False)
    e = G.number_of_edges()
    result = (type(e) == int)
    assert result


def test_sparse_matrix():
    """
    Test sparse_matrix. Call the function and check if the resulting matrix
    is a sparse matrix.
    If not, an AssertionError will raise.
    """
    result = (isspmatrix(sparse.sparse_matrix(show=False)))
    assert result

#-------------regression------------
def test_scatter_reg():
    """
    Test scatter_reg by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(regression.scatter_reg(1,1)) != int)
    assert result

def test_poly_fit():
    """
    Test poly_fit by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(regression.poly_fit(1,1)) != int)
    assert result

def test_R2():
    """
    Test R2 by running the function checking if R2 is different of 2.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(regression.R2(1,1)) != 2)
    assert result

# ---------- line charts ----------
def test_vactypedoses():
    """
    Test vactypedoses by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    """
    result = (type(line_charts.vactypedoses()) != int)
    assert result

def test_vacdoses():
    """
    Test vacdoses by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    """
    result = (type(line_charts.vacdoses()) != int)
    assert result
