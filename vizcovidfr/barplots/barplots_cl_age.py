import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_classe_age as pca
import os

T = load_datasets.Load_classe_age().save_as_df()

def bar_age(num_var, num_reg, save=False):
    """
    Display the bar plot of the given variable in the given region by age group today. Each variable and region have a special code that you can see in function parameters for details.

    Parameters
    ----------

    :param num_var: code of the variable you want to display. 
        Codes are in the following dictionnary.
    :type num_var: int
    :param num_reg: code of the region you want to display. 
        Codes are the official INSAA code region and are given in the dictionnary below.
    :type num_reg: int
    :param save: True if you want to save the graph in pdf file, False otherwise.
    :type save: bool, optionnal, default = False
    
    Variable dictionnary :

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
        number of people currently in Aftercare and Rehabilitation (SSR in french) or Long-Term Care Units (USLD in french).
    
    - Others :
        number of people currently hospitalized in another type of service.
    
    - Come back home :
        cumulative number of people who returned home.
    
    - Deaths :
        cumulative number of deceased persons.


    Region dictionnary :

        1 : Guadeloupe

        2 : Martinique

        3 : Guyane

        4 : La Reunion

        6 : Mayotte

        11 : Île-de-France

        24 : Centre-Val de Loire
    
        27 : Bourgogne-Franche-Comte

        28 : Normmandie

        32 : Hauts-de-France

        44 : Grand Est

        52 : Pays de la Loire

        53 : Bretagne

        75 : Nouvelle-Aquitaine

        76 : Occitanie

        84 : Auvergne-Rhône-Alpes

        93 : Provence-Alpes Côte d'Azur

        94 : Corse

    Returns
    ----------

    :return: Bar plot of one of the Covid variable in a specific region of France grouped by age.
    :rtype: plotly.graph_objects.bar.

    """
    T2 = pca.drop0(T)
    #Come back home and deaths are cumulative numbers, so we preprocess them in another dataframe.
    T_rad_dc = pca.reg(num_reg,T2).tail(10)
    T_rad_dc = pca.rename_cl(T_rad_dc)
    data_reg = pca.reg(num_reg, T2)
    dico_col = pca.dico_column(data_reg)
    data_reg_age = data_reg.groupby(by='cl_age90').sum()
    data_reg_age['cl_age90'] = data_reg_age.index
    data_reg_age = pca.rename_cl(data_reg_age)
    dico_file = pca.dico_file()
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    #Come back home and deaths
    if num_var == 6 or num_var ==7:
            fig = px.bar(T_rad_dc, x = 'cl_age90', y = dico_col[num_var], 
            hover_data = [dico_col[num_var]],
            color = dico_col[num_var],
            labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'cl_age90':'Age'},
            height = 400,
            title="Bar plot of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + " by age group today")
            fig.show()
    else:
            fig = px.bar(data_reg_age, x = 'cl_age90', y = dico_col[num_var], 
            hover_data = [dico_col[num_var]],
            color = dico_col[num_var],
            labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'cl_age90':'Age'},
            height = 400,
            title="Bar plot of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + " by age group today")
            fig.show()
    #Saving pdf file
    if save == True:
            fig.write_image(f"bar_age_{dico_file[num_var]}_{dico_reg[num_reg]}.pdf")


def bar_reg(num_var, save=False):
    """
    Display the bar plot of the given variable by region group today. Each variable and region have a special code that you can see in function parameters for details.

    Parameters
    ----------

    :param num_var: code of the variable you want to display. 
        Codes are in the following dictionnary.
    :type num_var: int
    :param save: True if you want to save the graph in pdf file, False otherwise.
    :type save: bool, optionnal, default = False

    - Variable dictionnary :

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
        number of people currently in Aftercare and Rehabilitation (SSR in french) or Long-Term Care Units (USLD in french).
    
    - Others :
        number of people currently hospitalized in another type of service.
    
    - Come back home :
        cumulative number of people who returned home.
    
    - Deaths :
        cumulative number of deceased persons.


    - Region codes (official INSAA) :


        1 : Guadeloupe

        2 : Martinique

        3 : Guyane

        4 : La Reunion

        6 : Mayotte

        11 : Île-de-France

        24 : Centre-Val de Loire
    
        27 : Bourgogne-Franche-Comte

        28 : Normmandie

        32 : Hauts-de-France

        44 : Grand Est

        52 : Pays de la Loire

        53 : Bretagne

        75 : Nouvelle-Aquitaine

        76 : Occitanie

        84 : Auvergne-Rhône-Alpes

        93 : Provence-Alpes Côte d'Azur

        94 : Corse


    Returns
    ----------

    :return: Bar plot of one of the Covid variable by region group.
    :rtype: plotly.graph_objects.bar.

    """
    T2 = pca.drop0(T)
    T_rad_dc = pca.rad_dc(T)
    data_day =T2.groupby(by='reg').sum()
    dico_file = pca.dico_file()
    dico_col = pca.dico_column(T2)
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    #Come back home and deaths are cumulative number, so we take the value of the last day recorded
    if num_var == 6 or num_var == 7:
            fig = px.bar(T_rad_dc, x=T_rad_dc['reg'], y=dico_col[num_var], color=dico_col[num_var], labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'reg': 'Region in France'}, height = 400, title="Bar plot of" + " " + dico_var[dico_col[num_var]] + " by region group today")
            fig.update_xaxes(type='category')
            fig.show()
    else:
            fig = px.bar(data_day, x=data_day.index, y=dico_col[num_var], color=dico_col[num_var], labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'reg': 'Region in France'}, height = 400, title="Bar plot of" + " " + dico_var[dico_col[num_var]] + " by region group today")
            fig.update_xaxes(type='category')
            fig.show()
    if save == True:
            fig.write_image(f"bar_reg_{dico_file[num_var]}.pdf")


