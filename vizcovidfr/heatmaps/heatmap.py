# ---------- requirements ----------
from download import download
import pandas as pd
import seaborn as sns
import plotly.express
import time

# local reqs
from vizcovidfr.loads.load_datasets import Load_posquotfr,Load_posquotreg,Load_posquotdep
from vizcovidfr.loads.load_datasets import Load_poshebreg,Load_poshebfr,Load_incregrea,Load_hopage
from vizcovidfr.preprocesses.preprocess_positivity import granupositivity
import matplotlib.pyplot as plt



def S2020_2021(semaine):
    """

    Number of the week

    Parameters
    ----------
    :param semaine: A specific week ("2020-S45")
    :type semaine: str


    Returns
    -------
    :return: number of the week

    :Examples:
    >>> S200_2021("2020-S35")
    """
    return int(semaine[3])*53+int(semaine[6:8])

def W2020_2021(number):
    """

    The week  of the year

    Parameters
    ----------
    :param number: A specific number
    :type number: int


    Returns
    -------
    :return: week of the year

    :Examples:
    >>> W200_2021("2020-S35")
    """

    if number==53:
        return "202"+str(number//54)+f"-S{number:02}"
    return "202"+str(number//54)+f"-S{number%53:02}"

def heatmapageday(df,debut,fin=None,weekday="jour"):
    """

    Give the heatmap by age class and day for incidence rate
    
    Parameters
    ----------
    :param df:  A dataframe of positivity for a territory

    :param debut: a month or a day ('2020-11')
    :type debut: str

    :param fin: a day the end of the interval
    :type fin: str,optional,default=None

    :param weekday: frequency "jour" or "week"
    :type weekday: str,optional,default="jour"


    Returns
    -------
    :return: A heatmap with two axis: one for age and one for day


    :Examples:
    >>> heatmapageday(granupositivity(Load_posquotreg().save_as_df(),1,"reg"),"2020-11")

    """

    df[weekday] = pd.to_datetime(df[weekday])
    df= df.set_index(weekday)
    df["incid"]=df["P"]/df['pop']*100000
    if weekday=="jour":
        if fin is None:
            df=df[debut][['incid','cl_age90']].reset_index()
        else:
            df=df[debut:fin][['incid','cl_age90']].reset_index()
        df[weekday]=pd.to_datetime(df['jour']).dt.date
    elif weekday=="week":
        a=[W2020_2021(i) for i in range(S2020_2021(debut),S2020_2021(fin)+1)]
        df=df[df[weekday].isin(a)]

    df.drop(df.loc[df["cl_age90"]==0].index,inplace=True)
    sns.heatmap(df.pivot(weekday,"cl_age90","incid"))
    plt.show()

def heatmapregage(df,granu,weekday):
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
    if len(weekday)>8:
        df=df.loc[df["jour"]==weekday]
    else:
        df=df.loc[df["week"]==weekday]
    df["incid"]=df["P"]/df['pop']*100000
    df.drop(df.loc[df["cl_age90"]==0].index,inplace=True)
    sns.heatmap(df.pivot(granu,"cl_age90","incid"))
    plt.show()

def heatmapregday(df,age,debut,granu="reg",weekday="jour",fin=None):
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
    df=df.loc[df["cl_age90"]==age]
    df['incid']=df['P']/df['pop']*100000
    if weekday =="jour":

        df[weekday] = pd.to_datetime(df[weekday])
        df=df.set_index(weekday)
        if fin is None:
            df=df[debut][['incid',granu,'cl_age90']].reset_index()
        else:
    
            df=df[debut:fin][['incid',granu,'cl_age90']].reset_index()

        df[weekday] = pd.to_datetime(df['jour']).dt.date
    elif weekday =="week":
        a=[W2020_2021(i) for i in range(S2020_2021(debut),S2020_2021(fin)+1)]
        df=df[df['week'].isin(a)]
    sns.heatmap(df.pivot(weekday,granu,"incid"))
    plt.show()

def incregrea(debut,fin=None):
    """

    Give the heatmap by age class and regions for incidence in intesive care
    
    Parameters
    ----------
    :param debut: a month or a day ('2020-11')
    :type debut: str

    :param fin: a day the end of the interval
    :type fin: str,optional,default=None




    Returns
    -------
    :return: A heatmap with two axis: one for age and one for regions


    :Examples:
    >>> incregrea("2020-11")

    """
    df=Load_incregrea().save_as_df()

    df["jour"] = pd.to_datetime(df["jour"])
    df= df.set_index('jour')
    if fin is None:
        df=df[debut].reset_index()
    else:
        df=df[debut:fin].reset_index()
    df["jour"] = pd.to_datetime(df['jour']).dt.date

    sns.heatmap(df.pivot("jour","numReg","incid_rea"))
    plt.show()
#%%

def hopage(chiffre,modes,debut):
    """

    Give the heatmap that you chose between "reg-age","reg-jour",
    "age-jour"
    
    Parameters
    ----------
    :param chiffre: to chose between "hosp","rea", "rad","dc"
    :type chiffre: str

    :param debut: a month or a day
    :type debut: str

    :param modes: to chose between "reg-age","reg-jour",
    "age-jour"
    :type modes: str




    Returns
    -------
    :return: the heatmap that you chose between "reg-age","reg-jour",
    "age-jour" for a certain period of time

    :Examples:
    >>> incregrea("2020-11")

    """
    dfhopage=Load_hopage().save_as_df()
    if modes=="reg-age":
        dfhopage=dfhopage.loc[dfhopage["jour"]==debut]
        dfhopage.drop(dfhopage.loc[dfhopage["cl_age90"]==0].index,inplace=True)

        sns.heatmap(dfhopage.pivot("cl_age90","reg",chiffre))

    if modes=="reg-jour":
        dfhopage["jour"] = pd.to_datetime(dfhopage["jour"])
        dfhopage= dfhopage.set_index('jour')
        dfhopage=dfhopage[debut].reset_index()
        dfhopage["jour"] = pd.to_datetime(dfhopage['jour']).dt.date
        dfhopage=dfhopage.loc[dfhopage["cl_age90"]==0]

        sns.heatmap(dfhopage.pivot("jour","reg",chiffre))

    if modes=="age-jour":
        dfhopage["jour"] = pd.to_datetime(dfhopage["jour"])
        dfhopage.drop(dfhopage.loc[dfhopage["cl_age90"]==0].index,inplace=True)

        dfhopage= dfhopage.set_index('jour')
        dfhopage=dfhopage[debut].reset_index()
        dfhopage["jour"] = pd.to_datetime(dfhopage['jour']).dt.date
        dfhopage=dfhopage.groupby(["jour","cl_age90"]).sum().reset_index()
        sns.heatmap(dfhopage.pivot("cl_age90","jour",chiffre))
    plt.show()


