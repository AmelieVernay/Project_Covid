# ---------- requirements ----------
from scipy.sparse import isspmatrix

# local reqs
from vizcovidfr.maps import maps
from vizcovidfr.sparse import sparse
from vizcovidfr.regression import regression
from vizcovidfr.line_charts import line_charts
from vizcovidfr.barplots import barplots_cl_age
from vizcovidfr.pie_charts import pie_chart


# ---------- maps ----------
def test_viz2Dmap():
    """
    Test viz2Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    ---
    Fonctions/methods that will be tested by extension:
        - load_datasets.Load_chiffres_cles().save_as_df()
        - preprocess_chiffres_cles.drop_some_columns()
        - preprocess_chiffres_cles.reg_depts()
        - preprocess_chiffres_cles.reg_depts_code_format()
        - preprocess_maps.map_save_path_routine(file_path)
    """
    result = (type(maps.viz2Dmap(file_path='')) != int)
    assert result


def test_viz3Dmap():
    """
    Test viz3Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    ---
    Fonctions/methods that will be tested by extension:
        - load_datasets.Load_chiffres_cles().save_as_df()
        - preprocess_chiffres_cles.drop_some_columns()
        - preprocess_chiffres_cles.reg_depts()
        - preprocess_chiffres_cles.reg_depts_code_format()
        - preprocess_maps.map_save_path_routine(file_path)
    """
    result = (type(maps.viz3Dmap(file_path='')) != int)
    assert result


def test_transfer_map():
    """
    Test transfer_map by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    ---
    Fonctions/methods that will be tested by extension:
        - load_datasets.Load_transfer().save_as_df()
        - preprocess_maps.map_save_path_routine(file_path)
    """
    result = (type(maps.transfer_map(file_path='')) != int)
    assert result


def test_vacmap():
    """
    Test vacmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    ---
    Fonctions/methods that will be tested by extension:
        - load_datasets.Load_vaccination().save_as_df()
        - preprocess_maps.map_save_path_routine(file_path)
    """
    result = (type(maps.vacmap(file_path='')) != int)
    assert result


# ---------- sparse ----------
def test_sparse_graph():
    """
    Test sparse_graph. Call the function and check if the number of edges
    of the resulting graph is an integer.
    If not, an AssertionError will raise.
    ---
    Fonctions/methods that will be tested by extension:
        - load_datasets.Load_transfer().save_as_df()
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
    ---
    Fonctions/methods that will be tested by extension:
        - load_datasets.Load_transfer().save_as_df()
    """
    result = (isspmatrix(sparse.sparse_matrix(show=False)))
    assert result


# ---------- regression ----------
def test_scatter_reg():
    """
    Test scatter_reg by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(regression.scatter_reg(1, 1)) != int)
    assert result


def test_poly_fit():
    """
    Test poly_fit by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(regression.poly_fit(1, 1)) != int)
    assert result


def test_R2():
    """
    Test R2 by running the function checking if R2 is different of 2.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    ---
    Fonctions/methods that will be tested by extension:
        -load_datasets.Load_Vaccine_storage().save_as_df()
    """
    result = (type(regression.R2(1, 1)) != 2)
    assert result


# ---------- line charts ----------
def test_vactypedoses():
    """
    Test vactypedoses by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    ---
    Functions/methods that will be tested by extension:
        - load_datasets.Load_Vaccine_storage().save_as_df()
    """
    result = (type(line_charts.vactypedoses()) != int)
    assert result


def test_vacdoses():
    """
    Test vacdoses by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    ---
    Functions/methods that will be tested by extension:
        - load_datasets.Load_Vaccine_storage().save_as_df()
    """
    result = (type(line_charts.vacdoses()) != int)
    assert result


# ----------- barplots ---------------
def test_bar_age():
    """
    Test bar_age by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(barplots_cl_age.bar_age(1, 1)) != int)
    assert result


def test_bar_reg():
    """
    Test bar_reg by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    """
    result = (type(barplots_cl_age.bar_reg(1)) != int)
    assert result


# ----------- pie chart ---------------
def test_piechart():
    """
    Test piechart by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will raise.
    ---
    Functions/methods that will be tested by extension:
        - load_datasets.Load_chiffres_cles().save_as_df()
        - preprocess_chiffres_cles.drop_some_columns()
        - preprocess_chiffres_cles.reg_depts()
    """
    result = (type(pie_chart.piechart()) != int)
    assert result
