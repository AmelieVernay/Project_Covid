#%%
import time
import numpy as np
import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_classe_age as pca

from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
model = LinearRegression()

# add python option to avoid "false positive" warning:
pd.options.mode.chained_assignment = None  # default='warn'

T = load_datasets.Load_classe_age().save_as_df()


def scatter_reg(num_var, num_reg):
    """
    Display the scatter plot of the evolution of the given variable in the
    given region. Each variable and region have a special code that you can
    see in function parameters for details.

    Parameters
    ----------

    :param num_var: code of the variable you want to display. Codes are in\
    the following dictionnary :

    1 : Hospitalization

    2 : Reanimation

    3 : Conventional hospitalization

    4 : SSR and USLD

    5 : Others

    6 : Come back home

    7 : Deaths

        - Hospitalization :
            number of hospitalized patients.

        - Reanimation :
            number of people currently in intensive care or intensive care.

        - Conventional hospitalization :
            number of people currently in conventional hospitalization.

        - SSR and USLD :
            number of people currently in Aftercare and Rehabilitation \
            (SSR in french) or Long-Term Care Units (USLD in french).

        - Others :
            number of people currently hospitalized in another type of service.

        - Come back home :
            cumulative number of people who returned home.

        - Deaths :
            cumulative number of deceased persons.

    :type num_var: int (from 1 to 7)

    :param num_reg: code of the region you want to display. Codes are in\
    the following dictionnary (official INSAA code) :

    1 : Guadeloupe

    2 : Martinique

    3 : Guyane

    4 : La Réunion

    6 : Mayotte

    11 : Île-de-France

    24 : Centre-Val de Loire

    27 : Bourgogne-Franche-Comte

    28 : Normandie

    32 : Hauts-de-France

    44 : Grand Est

    52 : Pays de la Loire

    53 : Bretagne

    75 : Nouvelle-Aquitaine

    76 : Occitanie

    84 : Auvergne-Rhône-Alpes

    93 : Provence-Alpes Côte d'Azur

    94 : Corse

    :type num_reg: int

    Returns
    ----------

    :return: Scatter plot of the evolution of one of the Covid variable in
        a specific region of France.
    :rtype: plotly.graph_objects.Scatter

    """
    start = time.time()
    # extracting chosen region
    T2 = pca.reg(num_reg, T)
    # converting to datetime format
    T2 = pca.date_time(T2)
    dico_col = pca.dico_column(T2)
    # grouping by day
    covid_day = pca.covid_day_fct(T2)
    # creating dictionnaries
    dico_reg = pca.dico_reg()
    dico_var = pca.dico_var()
    # scatter plot
    fig = px.scatter(
                covid_day,
                x=covid_day.index,
                y=dico_col[num_var],
                opacity=0.65,
                trendline_color_override='darkblue',
                labels={
                    dico_col[num_var]: dico_var[dico_col[num_var]],
                    'index': 'Date'},
                title="Scatter plot of the evolution of" +
                      " " +
                      dico_var[dico_col[num_var]] +
                      " in " +
                      dico_reg[num_reg])
    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))
    fig.show()


def poly_fit(num_var, num_reg):
    """
    Display the scatter plot of the evolution of the given variable in the
    given region with a polynomial regression. Each variable and region have
    a special code that you can see in function parameters for details.
    Degree of polynom is chosen by minimizing the mean squared error
    and is displayed as well.

    Parameters
    ----------

    :param num_var: code of the variable you want to display.
        Codes are in the following dictionnary :

    1 : Hospitalization

    2 : Reanimation

    3 : Conventional hospitalization

    4 : SSR and USLD

    5 : Others

    6 : Come back home

    7 : Deaths

        - Hospitalization :
            number of hospitalized patients.

        - Reanimation :
            number of people currently in intensive care or intensive care.

        - Conventional hospitalization :
            number of people currently in conventional hospitalization.

        - SSR and USLD :
            number of people currently in Aftercare and Rehabilitation
            (SSR in french) or Long-Term Care Units (USLD in french).

        - Others :
            number of people currently hospitalized in another type of service.

        - Come back home :
            cumulative number of people who returned home.

        - Deaths :
            cumulative number of deceased persons.

    :type num_var: int (from 1 to 7)

    :param num_reg: code of the region you want to display. Codes are in
        the following dictionnary (official INSAA code) :

    1 : Guadeloupe

    2 : Martinique

    3 : Guyane

    4 : La Réunion

    6 : Mayotte

    11 : Île-de-France

    24 : Centre-Val de Loire

    27 : Bourgogne-Franche-Comte

    28 : Normandie

    32 : Hauts-de-France

    44 : Grand Est

    52 : Pays de la Loire

    53 : Bretagne

    75 : Nouvelle-Aquitaine

    76 : Occitanie

    84 : Auvergne-Rhône-Alpes

    93 : Provence-Alpes Côte d'Azur

    94 : Corse

    :type num_reg: int

    Returns
    ----------

    :return: Scatter plot of the evolution of one of the Covid variable
        in a specific region of France with the regression line.
    :rtype: plotly.graph_objects.plot

    """
    start = time.time()
    R = pca.reg(num_reg, T)
    R = pca.date_time(R)
    dico_col = pca.dico_column(R)
    covid_day = pca.covid_day_fct(R)
    x = np.arange(0, covid_day.shape[0])
    y = covid_day[dico_col[num_var]]
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    dico_days = pca.dico_day(covid_day)
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    covid_day = covid_day.reset_index(drop=True)
    rmselist, x_p_list, y_poly_pred_P_list = pca.rmse_list(x, y)
    deg = list(rmselist).index(rmselist.min())
    fig = plt.scatter(dico_days.values(), y)
    plt.plot(dico_days.values(),
             y_poly_pred_P_list[deg],
             color='r')
    plt.suptitle("Polynomial regression of" +
                 " " +
                 dico_var[dico_col[num_var]] +
                 " in " +
                 dico_reg[num_reg]).set_fontsize(15)
    blue_line = mlines.Line2D(
                          [], [], color='blue',
                          markersize=15,
                          marker='.', label=dico_var[dico_col[num_var]])
    red_line = mlines.Line2D(
                          [], [], color='red',
                          markersize=15, label='Regression curve')
    plt.legend(handles=[blue_line, red_line])
    plt.title(f'Degree of polynomial regression : {deg+1}', fontsize=10)
    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))
    plt.show()


def R2(num_var, num_reg):
    """
    Display the R2 of the polynomial regression made by poly_fit function.
    Arguments are the same than poly_fit.

    Parameters
    ----------

    :param num_var: code of the variable you want to display.
        Codes are in the following dictionnary :

    1 : Hospitalization

    2 : Reanimation

    3 : Conventional hospitalization

    4 : SSR and USLD

    5 : Others

    6 : Come back home

    7 : Deaths

        - Hospitalization :
            number of hospitalized patients.

        - Reanimation :
            number of people currently in intensive care or intensive care.

        - Conventional hospitalization :
            number of people currently in conventional hospitalization.

        - SSR and USLD :
            number of people currently in Aftercare and Rehabilitation
            (SSR in french) or Long-Term Care Units (USLD in french).

        - Others :
            number of people currently hospitalized in another type of service.

        - Come back home :
            cumulative number of people who returned home.

        - Deaths :
            cumulative number of deceased persons.

    :type num_var: int (from 1 to 7)

    :param num_reg: code of the region you want to display.
        Codes are in the following dictionnary (official INSAA code) :

    1 : Guadeloupe

    2 : Martinique

    3 : Guyane

    4 : La Réunion

    6 : Mayotte

    11 : Île-de-France

    24 : Centre-Val de Loire

    27 : Bourgogne-Franche-Comte

    28 : Normandie

    32 : Hauts-de-France

    44 : Grand Est

    52 : Pays de la Loire

    53 : Bretagne

    75 : Nouvelle-Aquitaine

    76 : Occitanie

    84 : Auvergne-Rhône-Alpes

    93 : Provence-Alpes Côte d'Azur

    94 : Corse

    :type num_reg: int

    Returns
    ----------

    :return: Scatter plot of the evolution of one of Covid variable
        in a specific region of France.
    :rtype: plotly.graph_objects.Scatter

    """
    start = time.time()
    R = pca.reg(num_reg, T)
    R = pca.date_time(R)
    dico_col = pca.dico_column(R)
    covid_day = pca.covid_day_fct(R)
    x = np.arange(0, covid_day.shape[0])
    y = covid_day[dico_col[num_var]]
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    covid_day = covid_day.reset_index(drop=True)
    rmselist, x_p_list, y_poly_pred_P_list = pca.rmse_list(x, y)
    deg = list(rmselist).index(rmselist.min())
    res = 'R2 of polynomial regression of ' + dico_var[dico_col[num_var]] + \
          ' in ' + dico_reg[num_reg] + \
         f' is : {r2_score(y,y_poly_pred_P_list[deg])}.'
    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))
    return res
