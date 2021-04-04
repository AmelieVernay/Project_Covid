import pandas as pd
import matplotlib.pyplot as plt
from download import download
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#url_db = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
url_db="https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv"
url_fr="https://static.data.gouv.fr/resources/donnees-relatives-a-lepidemie-de-covid-19-en-france-vue-densemble/20210404-140127/synthese-fra.csv"
path_target = "./chiffres-cles.csv"
class Load_covid:
    def __init__(self, url=url_db, target_name=path_target):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df_covid = pd.read_csv(path_target)
        date = df_covid['date']
        a = list((date[:]))
        b = list(map(lambda x: datetime.date(int(x[:4]),int(x[5:7]), int(x[8:])).\
        isoformat(),a))
        b = pd.DatetimeIndex(b)
        df_covid.loc[:, 'date'] = b
        df_covid = df_covid.set_index('date')
        df_covid
        return df_covid['2020-01-24':]
    
    
def keysubtablename(nom):
    df_covid=Load_covid().save_as_df()
    if nom in ["departements","pays","region"]:
        dfsub = df_covid.loc[df_covid['granularite']==nom]
    else:
        dfsub = df_covid.loc[df_covid['maille_nom']==nom]
    dfsub = dfsub[~dfsub.index.duplicated(keep='first')]
    return dfsub

def keyseries(nom,chiffre,evo=True):

    fr=nom=="France"
    if chiffre in ["deces_à_l'hôpital","deceshop"]:
        chiffre="total_deces_hopital"
        fr=True 
        print("données pour la France entière")

    if fr:
        download(url_fr,"./chiffres-fr.csv",replace=True)
        df_covid=pd.read_csv("./chiffres-fr.csv")
        date = df_covid['date']
        a = list((date[:]))
        b = list(map(lambda x: datetime.date(int(x[:4]),int(x[5:7]), int(x[8:])).\
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
    if evo:
        return keysubtablename(nom)[chiffre].dropna().diff()
    return keysubtablename(nom)[chiffre].dropna()


def plotseries(series,average=True):
    sns.set(rc={'figure.figsize':(11, 4)})
    if average:
        ax=series.rolling(window=7).mean().plot()
    else:
        ax=series.plot()
    return ax
    
def keyplot(nom,chiffre,evo=True,average=True):
    ax=plotseries(keyseries(nom,chiffre,evo),average)
    ax.set(title= " number of "+chiffre+ " with time",ylabel=chiffre)

keyplot("France","cas",evo=False)
    

keyseries("France","hôpital",evo=False)
