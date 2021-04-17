# ---------- requirements ----------

import pandas as pd
from download import download
pd.options.display.max_rows = 25
import datetime
import plotly.express as px

#from vizcovidfr.loads import load_datasets



##Vaccination part
#line chart with number of vaccinated people in the whole France

#line chart which represents the french vaccine storage per vaccine type 

url = "https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-stocks-des-doses-de-vaccins-contre-la-covid-19/#_"
path_target = "C:/Users/quenf/vizcovidfr/vizcovidfr/data/stocks-es-national.csv"
#download(url, path_target, replace = True)

def vactypedoses(vaccine_type):
    '''
    Make an animated line chart of France vaccine data.

    :param vaccine_type: the vaccine type we want to display.
        Should be either 'Pfizer', 'Moderna', 'AstraZeneca' or 'All vaccines'.
        You can hover your mouse over the curves to get thorough information. 
    :type vaccine_type: string
    :return: an animated line chart representing the actual 
    dose number and the actual cdu (common dispensing units) 
    number, of the chosen vaccine type (in storage).
    '''
    df_Vac_type = pd.read_csv(path_target, sep = ",")
    df_Vac_type2 = df_Vac_type.groupby(['type_de_vaccin'])
    pfizer = df_Vac_type2.get_group('Pfizer').reset_index(drop = True)
    mdn = df_Vac_type2.get_group('Moderna').reset_index(drop = True)
    astra = df_Vac_type2.get_group('AstraZeneca').reset_index(drop = True)
    
    # choose dataframe according to vaccine_type argument 
    if (vaccine_type == 'Pfizer'):
        df = pfizer.copy()
        vac_type = 'Pfizer'
        fig = px.line(df, x = 'date', y = ['nb_doses', 'nb_ucd'], title = 'Pfizer storage in France')
    elif (vaccine_type == 'Moderna'):
        df = mdn.copy()
        vac_type = 'Moderna'
        fig = px.line(df, x = 'date', y = ['nb_doses', 'nb_ucd'], title = 'Moderna storage in France')
    elif (vaccine_type == 'AstraZeneca'):
        df = astra.copy()
        vac_type == 'AstraZeneca'
        fig = px.line(df, x = 'date', y = ['nb_doses', 'nb_ucd'], title = 'AstraZeneca storage in France')
    elif (vaccine_type == 'All vaccines'):
        df = df_Vac_type.copy()
        vac_type = 'ALL'
        fig = px.line(df, x = 'date', y = ['nb_doses', 'nb_ucd'], color = 'type_de_vaccin', title = 'Vaccine storage in France')
    # displaying line chart according to vaccine_type argument
    fig.show()

#Rather choosing the variables ('nb_doses' and 'nb_ucd') 
#as arguments or in the animation?

#how to display the year of each date?


#Test
vactypedoses(vaccine_type = 'Moderna')

#line chart with total number of vaccine doses


def vacdoses(number):
    '''
    Make an interactive line chart of France vaccine data.

    :param number: the type of dose units we want to display.
        Should be either doses or cdu.
    :type number: string
    :return: an interactive line chart representing the actual
    amount in storage of vaccine doses, according to the chosen 
    unit.
    '''
    df_Vac_type = pd.read_csv(path_target, sep = ",")
    df = df_Vac_type.groupby(['date'])['nb_doses', 'nb_ucd'].agg('sum').reset_index()
    doses = df.groupby(['date'])['nb_doses'].size().reset_index()
    ucd = df.groupby(['date'])['nb_ucd'].size().reset_index()
    doses['nb_doses'] = df['nb_doses']
    ucd['nb_ucd'] = df['nb_ucd']
    if (number == 'doses'):
        df = doses.copy()
        nbr = 'nb_doses'
    else:
        df = ucd.copy()
        nbr = 'nb_ucd'
    #displaying a line chart according to number argument
    fig = px.line(df, x = 'date', y = nbr, title = 'Vaccine storage in France')
    fig.show()

#Test
#vacdoses(number = 'cdu')

#change name of the function and of the argument
#changedocstring

