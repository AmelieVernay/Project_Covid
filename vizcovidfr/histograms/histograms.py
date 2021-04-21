import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_classe_age as pca

T = load_datasets.Load_classe_age().save_as_df()


def hist_age(num_var, num_reg):
    """
    Display the bar plot of the given variable in the given region by age
    group today. Each variable and region have a special code that you can
    see in function parameters for details.

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

    :return: Bar plot of one of the Covid variable in a specific region of
        France grouped by age.
    :rtype: plotly.graph_objects.bar

    """
    T2 = pca.drop0(T)
    data_reg = pca.reg(num_reg, T2)
    dico_col = pca.dico_column(data_reg)
    data_reg_age = data_reg.groupby(by='cl_age90').sum()
    data_reg_age['cl_age90'] = data_reg_age.index
    data_reg_age['cl_age90'] = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '+90']
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    fig = px.bar(data_reg_age, x = 'cl_age90', y = dico_col[num_var],
                hover_data = [dico_col[num_var]],
                color = dico_col[num_var],
                labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'cl_age90':'Age'},
                height = 400,
                title="Bar plot of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + " by age group today")
    fig.show()
