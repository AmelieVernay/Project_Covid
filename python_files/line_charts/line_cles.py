import pandas as pd
import matplotlib.pyplot as plt
from download import download
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#url_db = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
url_db="https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv"
url_fr="https://www.data.gouv.fr/fr/datasets/r/d3a98a30-893f-47f7-96c5-2f4bcaaa0d71"
path_target = "../data/chiffres-cles.csv"
class Load_covid:
    """
    A class that allows you to download and format the dataset 
    containing the counts of diverse figures describing the 
    spread of the pandemic in France.

    """
    def __init__(self, url=url_db, target_name=path_target):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        """
        Nicely formatted dataframe with time indexation.
        """
        df_covid = pd.read_csv(path_target)
        date = df_covid['date']
        a = list((date[:]))
        b = list(map(lambda x: datetime.date(int(x[:4]),\
        int(x[5:7]), int(x[8:])).\
        isoformat(),a))
        b = pd.DatetimeIndex(b)
        df_covid.loc[:, 'date'] = b
        df_covid = df_covid.set_index('date')
        df_covid
        return df_covid['2020-01-24':]
    
    
def keysubtablename(nom):
    """
    nom: A part of France or a partition

    Function that extract the data for a certain 
    granularity or territory and remove repetitions.
    """
    df_covid=Load_covid().save_as_df()
    if nom in ["departements","pays","region"]:
        dfsub = df_covid.loc[df_covid['granularite']==nom]
    else:
        dfsub = df_covid.loc[df_covid['maille_nom']==nom]
    dfsub = dfsub[~dfsub.index.duplicated(keep='first')]
    return dfsub

def keyseries(nom,chiffre,evo=True):
    """

    nom: A part of France
    chiffre: A figure
    evo: New per day or cumulative

    Give the time series of the figure of interest

    """
    fr=nom=="France"
    if chiffre in ["deces_à_l'hôpital","deceshop"]:
        chiffre="total_deces_hopital"
        fr=True 
        print("données pour la France entière")

    if fr:
        download(url_fr,"../data/chiffres-fr.csv",replace=True)
        df_covid=pd.read_csv("./chiffres-fr.csv")
        date = df_covid['date']
        a = list((date[:]))
        b = list(map(lambda x: datetime.date(int(x[:4]),int(x[5:7]),\
         int(x[8:])).\
        isoformat(),a))
        b = pd.DatetimeIndex(b)
        df_covid.loc[:, 'date'] = b
        df_covid = df_covid.set_index('date')
    if chiffre in ["cas","nombre_de_cas","cas_confirmes"]:
        chiffre="cas_confirmes"
        if fr:
            chiffre="total_cas_confirmes"
    elif chiffre in ["hospitalisation","hôpital","hospitalises"]:
        chiffre="hospitalises"
        if fr:
            chiffre="patients_hospitalises"
    elif chiffre in ["deces_ehpad"]:
        if fr:
            chiffre="total_deces_ehpad"
    elif chiffre in ["morts"]:
        chiffre="deces"
    elif chiffre in ["reanimation"]:
        if fr:
            chiffre="patients_reanimation"

    elif chiffre in ["cas_confirmes_ehpad"]:
        if fr:
            chiffre="total_cas_confirmes_ephad"
    elif chiffre in ["gueris"]:
        if fr:
            chiffre="total_patients_gueris"
    if fr:
        if evo:
            return df_covid[chiffre].diff()
        return df_covid[chiffre]
    elif chiffre in ["cas_confirmes"]:
        urlposreg="https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
        pathtarget="../data/posquotreg.csv"
        download(urlposreg,pathtarget,replace=True)
        dfposreg=pd.read_csv(pathtarget,sep=";")
        REGIONS = {
    'Auvergne-Rhône-Alpes': 84,
    'Bourgogne-Franche-Comté': 27,
    'Bretagne': 53,
    'Centre-Val de Loire': 24,
    'Corse': 94,
    'Grand Est':44 ,
    'Guadeloupe': 1,
    'Guyane': 3,
    'Hauts-de-France': 32,
    'Île-de-France': 11,
    'La Réunion': 4,
    'Martinique': 2,
    'Normandie': 28,
    'Nouvelle-Aquitaine': 75,
    'Occitanie': 76,
    'Pays de la Loire': 52,
    'Provence-Alpes-Côte d\'Azur': 93,}
        number=REGIONS[nom]

        df= dfposreg.loc[dfposreg["reg"]==number,:].groupby(['jour']).sum()
        df.index = pd.to_datetime(df.index)

        if evo:
            return df['P']
        else: return df['P'].cumsum()

    if evo:
        return keysubtablename(nom)[chiffre].dropna().diff()
    return keysubtablename(nom)[chiffre].dropna()


def plotseries(series,average=True):

    """

    series: a time series
    average: do the moving average or not

    Allows you to plot a time series wih or without a moving average


    """
    sns.set(rc={'figure.figsize':(11, 4)})
    if average:
        ax=series.rolling(window=7).mean().plot()
    else:
        ax=series.plot()
    return ax
    
def keyplot(nom,chiffre,evo=True,average=True):

    """
    nom: A part of France
    chiffre: A figure
    average: do the moving average or not
    evo: New per day or cumulative

    Plot the time series associates with figures of Covid-19.
    Take in acount the scale (country, region, ...)
    """
    ax=plotseries(keyseries(nom,chiffre,evo),average)
    if chiffre in ["cas","nombre_de_cas","cas_confirmes"] and not evo :
        ax.set(title= "Prevalence of Covid-19 in "+nom,ylabel="case")
    elif chiffre in ["cas","nombre_de_cas","cas_confirmes"] and evo:
        ax.set(title= "Daily cases of Covid-19 in "+nom,ylabel="case")
    elif chiffre in ["hospitalisation","hôpital","hospitalises"] and evo:
        ax.set(title= "Daily extra patients of Covid-19\
             at the hospital in "+nom,ylabel="people hospitalized")
    elif chiffre in ["hospitalisation","hôpital","hospitalises"] and not evo:
        ax.set(title= "Number of patients of Covid-19\
         at the hospital in "+nom,ylabel="people hospitalized")
    elif chiffre in["deces_ehpad"] and not evo:
        ax.set(title= "Number of death of Covid-19 \
            in EHPADs in "+nom,ylabel="death")
    elif chiffre in["deces_ehpad"] and  evo:
        ax.set(title= "Number of death of Covid-19 in\
             EHPADs in "+nom,ylabel="death")
    elif chiffre in["deces","morts"] and  not evo:
        ax.set(title= "Number of deaths of Covid-19 \
             in "+nom,ylabel="death")
    elif chiffre in["deces","morts"] and   evo:
        ax.set(title= "New deaths of Covid-19\
              in "+nom,ylabel="death")
    elif chiffre in["reanimation"] and   evo:
        ax.set(title= "Daily extra patients in\
             intensive care because of Covid-19  in "+nom,ylabel="patients")
    elif chiffre in["reanimation"] and not  evo:
        ax.set(title="Number of patients in intensive\
         care because of Covid-19 in"+nom,ylabel="patients")
    elif chiffre in ["cas_confirmes_ehpad"] and evo:
        ax.set(title="Daily cases of Covid-19 in\
         EHPADs"+nom,ylabel="cases")
    elif chiffre in ["cas_confirmes_ehpad"] and  not evo:
        ax.set(title="Prevalence of Covid-19 in\
             EHPADs"+nom,ylabel="cases")
    elif chiffre in ["gueris"] and  not evo:
        ax.set(title="Number of people cured from \
            Covid-19 "+nom,ylabel="people")
    elif chiffre in ["gueris"] and   evo:
        ax.set(title="Daily number of people \
            cured from Covid-19 "+nom,ylabel="people")


keyplot("France","cas",evo=True)
    
print('a')
keyseries("France","hôpital",evo=False)
print("b")
keyseries('Île-de-France','cas')
print("c")
keyplot('Île-de-France','cas')


