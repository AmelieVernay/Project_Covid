# ---------- requirements ----------
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


# ---
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_heatmaps
# ---


def heatmap_age(start, end=None, granularity='France', num_reg=1,
                frequency='daily'):
    """
    Give the heatmap by age class and day for incidence rate

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
    :param end: a day the end of the interval
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
    >>>

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

    # df[freq] = pd.to_datetime(df[freq])
    # df = df.set_index(freq)
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
    sns.heatmap(df.pivot(freq, "cl_age90", "incid"))
    plt.show()


heatmap_age(granularity='region', num_reg=76, frequency='weekly', start='2020-S21', end='2020-S51')


#def heatmapregage(df, granu, weekday):
#    """
#    Give the heatmap by age class and regions for incidence rate
#
#    Parameters
#    ----------
#    :param df:  A dataframe of positivity for a territory
#
#    :param granu: "reg " or "dep" (by departments it's difficult to read)
#    :type granu: str
#
#
#    :param weekday: a specific day
#    :type weekday: str
#
#    Returns
#    -------
#    :return: A heatmap with two axis: one for age and one for day
#
#
#    :Examples:
#    >>> heatmapregage(Load_posquotreg().save_as_df(),"reg","2020-11-06")
#
#
#    """
#    if len(weekday)>8:
#        df=df.loc[df["jour"]==weekday]
#    else:
#        df=df.loc[df["week"]==weekday]
#    df["incid"]=df["P"]/df['pop']*100000
#    df.drop(df.loc[df["cl_age90"]==0].index,inplace=True)
#    sns.heatmap(df.pivot(granu,"cl_age90","incid"))
#    plt.show()
#
#def heatmapregday(df,age,debut,granu="reg",weekday="jour",fin=None):
#    """
#
#    Give the heatmap by age class and regions for incidence rate
#
#    Parameters
#    ----------
#    :param df:  A dataframe of positivity for a territory
#
#    :param granu: "reg " or "dep" (by departments it's difficult to read)
#    :type granu: str
#
#    :param debut: a month or a day ('2020-11')
#    :type debut: str
#
#    :param fin: a day the end of the interval
#    :type fin: str,optional,default=None
#
#
#    :param weekday: frequency "jour" or "week"
#    :type weekday: str,optional,default="jour"
#    :param age: a age class
#    :type age: int
#
#
#    Returns
#    -------
#    :return: A heatmap with two axis: one for age and one for day
#
#
#    :Examples:
#    >>> heatmapregday(Load_posquotreg().save_as_df(),0,"2020-11")
#
#
#    """
#    df=df.loc[df["cl_age90"]==age]
#    df['incid']=df['P']/df['pop']*100000
#    if weekday =="jour":
#
#        df[weekday] = pd.to_datetime(df[weekday])
#        df=df.set_index(weekday)
#        if fin is None:
#            df=df[debut][['incid',granu,'cl_age90']].reset_index()
#        else:
#
#            df=df[debut:fin][['incid',granu,'cl_age90']].reset_index()
#
#        df[weekday] = pd.to_datetime(df['jour']).dt.date
#    elif weekday =="week":
#        a=[preprocess_heatmaps.W2020_2021(i) for i in range(preprocess_heatmaps.S2020_2021(debut),preprocess_heatmaps.S2020_2021(fin)+1)]
#        df=df[df['week'].isin(a)]
#    sns.heatmap(df.pivot(weekday,granu,"incid"))
#    plt.show()
#
## def incregrea(debut,fin=None):
#     """
#
#     Give the heatmap by age class and regions for incidence in intesive care
#
#     Parameters
#     ----------
#     :param debut: a month or a day ('2020-11')
#     :type debut: str
#
#     :param fin: a day the end of the interval
#     :type fin: str,optional,default=None
#
#
#
#
#     Returns
#     -------
#     :return: A heatmap with two axis: one for age and one for regions
#
#
#     :Examples:
#     >>> incregrea("2020-11")
#
#     """
#     df=Load_incregrea().save_as_df()
#
#     df["jour"] = pd.to_datetime(df["jour"])
#     df= df.set_index('jour')
#     if fin is None:
#         df=df[debut].reset_index()
#     else:
#         df=df[debut:fin].reset_index()
#     df["jour"] = pd.to_datetime(df['jour']).dt.date
#
#     sns.heatmap(df.pivot("jour","numReg","incid_rea"))
#     plt.show()
# #%%
#
# def hopage(chiffre,modes,debut):
#     """
#
#     Give the heatmap that you chose between "reg-age","reg-jour",
#     "age-jour"
#
#     Parameters
#     ----------
#     :param chiffre: to chose between "hosp","rea", "rad","dc"
#     :type chiffre: str
#
#     :param debut: a month or a day
#     :type debut: str
#
#     :param modes: to chose between "reg-age","reg-jour",
#     "age-jour"
#     :type modes: str
#
#
#
#
#     Returns
#     -------
#     :return: the heatmap that you chose between "reg-age","reg-jour",
#     "age-jour" for a certain period of time
#
#     :Examples:
#     >>> incregrea("2020-11")
#
#     """
#     dfhopage=Load_hopage().save_as_df()
#     if modes=="reg-age":
#         dfhopage=dfhopage.loc[dfhopage["jour"]==debut]
#         dfhopage.drop(dfhopage.loc[dfhopage["cl_age90"]==0].index,inplace=True)
#
#         sns.heatmap(dfhopage.pivot("cl_age90","reg",chiffre))
#
#     if modes=="reg-jour":
#         dfhopage["jour"] = pd.to_datetime(dfhopage["jour"])
#         dfhopage= dfhopage.set_index('jour')
#         dfhopage=dfhopage[debut].reset_index()
#         dfhopage["jour"] = pd.to_datetime(dfhopage['jour']).dt.date
#         dfhopage=dfhopage.loc[dfhopage["cl_age90"]==0]
#
#         sns.heatmap(dfhopage.pivot("jour","reg",chiffre))
#
#     if modes=="age-jour":
#         dfhopage["jour"] = pd.to_datetime(dfhopage["jour"])
#         dfhopage.drop(dfhopage.loc[dfhopage["cl_age90"]==0].index,inplace=True)
#
#         dfhopage= dfhopage.set_index('jour')
#         dfhopage=dfhopage[debut].reset_index()
#         dfhopage["jour"] = pd.to_datetime(dfhopage['jour']).dt.date
#         dfhopage=dfhopage.groupby(["jour","cl_age90"]).sum().reset_index()
#         sns.heatmap(dfhopage.pivot("cl_age90","jour",chiffre))
#     plt.show()
#
