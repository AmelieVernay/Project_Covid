# ---------- requirements ----------
#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# local reqs
#from vizcovidfr.loads.load_datasets import Load_posquotfr
#from vizcovidfr.loads.load_datasets import Load_posquotreg
#from vizcovidfr.loads.load_datasets import Load_posquotdep
#from vizcovidfr.loads.load_datasets import Load_poshebreg, Load_poshebfr
#from vizcovidfr.loads.load_datasets import Load_incregrea, Load_hopage
from vizcovidfr.preprocesses.preprocess_positivity import granupositivity
from vizcovidfr.preprocesses import preprocess_classe_age as pca

# ---
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_heatmaps
# ---


def heatmap_age(start, end=None, granularity='France', num_reg=1,
                frequency='daily'):
    """
    Make a heatmap by age class and the given frequency for incidence rate.

    Parameters
    ----------
    :param start:
        if frequency='daily':
            if end=None, must be a year and a month on the format 'YYYY-MM'
            else, must be a day on the format 'YYYY-MM-DD'
        if frequency='weekly':
            must be the week of a year on the format 'YYYY-SWW',
            and end is **not** optional and must be of the same format
    :type start: str
    :param end: date when the heatmap stops.
        Only if start is on format 'YYYY-MM-DD' or 'YYYY-SWW'.
        Must be on format 'YYYY-MM-DD' or 'YYYY-SWW', same than start.
        Must be a date later than start.
    :type end: NoneType or str, optional only if frequency='daily' and if
        start is of the format 'YYYY-MM'
    :param granularity: the granularity we want the heatmap to be based on.
        Should be either 'region' or 'France'.
    :type granularity: str, optional, default='France'
    :param num_reg: code of the region you want to display.
        Codes are the official INSAA code region and are given in the
        dictionary below.
    :type num_reg: int, optional (useful only if granularity='region'),
        default=Guadeloupe


    Region dictionary :

        1 : Guadeloupe

        2 : Martinique

        3 : Guyane

        4 : La Reunion

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


    :param frequency: the time frequency to show on the heatmap
    :type frequency: str, optional, default='daily'

    Returns
    -------
    :return: A heatmap with two axis: one for age and one for day
    :rtype: seaborn heatmap

    :Example:

    **Heatmap for the month of March 2021 in France**

    >>> heatmap_age(start='2021-03')

    **Heatmap between 2021-03-12 and 2021-04-10 in France**

    >>> heatmap_age(start='2021-03-12', end='2021-04-10')

    **Heatmap between week 3 and week 10 of the year 2021 in France**

    >>> heatmap_age(start='2021-S03', end='2021-S10', frequency='weekly')

    **Heatmap for the month of March 2021 in Martinique**

    >>> heatmap_age(start='2021-03', granularity='region', num_reg=2)

    """
    if ((granularity == 'France') & (frequency == 'weekly')):
        df = load_datasets.Load_poshebfr().save_as_df()
        freq = 'week'
    if ((granularity == 'France') & (frequency == 'daily')):
        df = load_datasets.Load_posquotfr().save_as_df()
        freq = 'jour'
    if ((granularity == 'region') & (frequency == 'daily')):
        df = granupositivity(load_datasets.Load_posquotreg().save_as_df(),
                             num_reg, "reg")
        freq = 'jour'
    if ((granularity == 'region') & (frequency == 'weekly')):
        df = granupositivity(load_datasets.Load_poshebreg().save_as_df(),
                             num_reg, "reg")
        freq = 'week'

    df["incid"] = df["P"]/df['pop']*100000
    if (freq == "jour"):
        df[freq] = pd.to_datetime(df[freq])
        df = df.set_index(freq)
        if end is None:
            df = df[start][['incid', 'cl_age90']].reset_index()
        else:
            df = df[start:end][['incid', 'cl_age90']].reset_index()
        df[freq] = pd.to_datetime(df['jour']).dt.date
    elif (freq == "week"):
        a = [preprocess_heatmaps.W2020_2021(i) for i in range(preprocess_heatmaps.S2020_2021(start), preprocess_heatmaps.S2020_2021(end)+1)]
        df = df[df[freq].isin(a)]

    df.drop(df.loc[df["cl_age90"] == 0].index, inplace=True)
    dico_reg = pca.dico_reg()
    if (granularity == 'region'):
        sns.heatmap(df.pivot(freq, "cl_age90", "incid"))
        plt.title(f'Incidence rate in ' + dico_reg[num_reg] + f' on a {frequency} time basis')
        plt.xlabel('Age')
        plt.ylabel('Time')
        plt.show()
    else:
        sns.heatmap(df.pivot(freq, "cl_age90", "incid"))
        plt.title(f'Incidence rate in France on a {frequency} time basis')
        plt.xlabel('Age')
        plt.ylabel('Time')
        plt.show()


heatmap_age(start='2020-05-02', end='2020-05-27')

#%%

def heatmap_reg_age(weekday):
    """
    Give the heatmap by age class and regions for incidence rate

    Parameters
    ----------
    :param df:  A dataframe of positivity for a territory

    :param granu: "reg " or "dep" (by departments it's difficult to read)
    :type granu: str


    :param weekday: a specific day
    :type weekday: str

    Returns
    -------
    :return: A heatmap with two axis: one for age and one for day


    :Examples:
    >>> heatmapregage(Load_posquotreg().save_as_df(),"reg","2020-11-06")


    """
    if  (len(weekday) > 8):
        df = load_datasets.Load_posquotreg().save_as_df()
    if   (len(weekday) <= 8):
        df = load_datasets.Load_poshebreg().save_as_df()
      
    if len(weekday) > 8:
        df = df.loc[df["jour"]==weekday]
    else:
        df = df.loc[df["week"]==weekday]
    df["incid"] = df["P"]/df['pop']*100000
    df.drop(df.loc[df["cl_age90"] == 0].index,inplace=True)
    sns.heatmap(df.pivot("reg","cl_age90","incid"))
    plt.show()

heatmap_reg_age("2020-11-12")
#%%
def heatmapregday(age,debut,fin=None,weekday="jour"):
    """

    Give the heatmap by age class and regions for incidence rate

    Parameters
    ----------
    :param df:  A dataframe of positivity for a territory

    :param granu: "reg " or "dep" (by departments it's difficult to read)
    :type granu: str

    :param debut: a month or a day ('2020-11')
    :type debut: str

    :param fin: a day the end of the interval
    :type fin: str,optional,default=None


    :param weekday: frequency "jour" or "week"
    :type weekday: str,optional,default="jour"
    :param age: a age class
    :type age: int


    Returns
    -------
    :return: A heatmap with two axis: one for age and one for day


    :Examples:
    >>> heatmapregday(Load_posquotreg().save_as_df(),0,"2020-11")


    """
    if weekday=="jour":
        df=load_datasets.Load_posquotreg().save_as_df()
    if weekday=="week":
        df=load_datasets.Load_poshebreg().save_as_df()

    df=df.loc[df["cl_age90"]==age]
    df['incid']=df['P']/df['pop']*100000
    if weekday =="jour":

        df[weekday] = pd.to_datetime(df[weekday])
        df=df.set_index(weekday)
        if fin is None:
            df=df[debut][['incid',"reg",'cl_age90']].reset_index()
        else:

            df=df[debut:fin][['incid',"reg",'cl_age90']].reset_index()

        df[weekday] = pd.to_datetime(df['jour']).dt.date
    elif weekday =="week":
        a=[preprocess_heatmaps.W2020_2021(i) for i in range(preprocess_heatmaps.S2020_2021(debut),preprocess_heatmaps.S2020_2021(fin)+1)]
        df=df[df['week'].isin(a)]
    sns.heatmap(df.pivot(weekday,"reg","incid"))
    plt.show()

heatmapregday(0,"2020-S36","2020-S52","week")
# %%
