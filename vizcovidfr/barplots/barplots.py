#%%
from download import download
import pandas as pd
from vizcovidfr.loads.load_datasets import Load_posquotfr,Load_posquotreg,Load_posquotdep
from vizcovidfr.loads.load_datasets import Load_poshebdep,Load_poshebreg,Load_poshebfr
from vizcovidfr.loads.load_datasets import Load_incquotdep,Load_incquotreg,Load_incquotfr
from vizcovidfr.loads.load_datasets import Load_inchebdep,Load_inchebreg,Load_inchebfr
from vizcovidfr.loads.load_datasets import Load_incregrea,Load_hopdep,Load_hopage,Load_hopsex
from vizcovidfr.preprocesses.preprocess_positivity import ignoreage,granupositivity
#%%

#dfposfr=ignoreage(Load_posquotfr().save_as_df())

#dfposfr["P_f"]
#dfposfr.loc["2020-05-13"]
#dfposfr['P']/dfposfr["T"]
#dfposfr

#%%
def compareHF(jour,chiffre,df):
    
    """

    Gives the positivity or number of test for male and female
    
    Parameters
    ----------
    :param jour: A specific day or a week ("2020-11-12","2020-S45")
    :type nom: str
    :param chiffre: positivity "P" or "T" test or even 'pop'

    :type chiffre: str

    :param df: A dataframe of positivity by any region or frequency
            with a specific age class 


    Returns
    -------
    :return: A list comparing two numbers refering to male and female
    :rtype: list 

    :Examples:
    >>> compareHF("2020-11-12","P",granupositvity(ignoreage(Load_incquotreg().save_as_df()),2,"reg"))


    """
    if not chiffre in ["hosp","rea","rad","dc"]:

        return [df.loc[jour,][chiffre+"_h"],df.loc[jour,][chiffre+"_f"]]
    else: 
        df=df.loc[jour,]
        return [df.loc[df["sexe"]==1][chiffre],df.loc[df["sexe"]==2][chiffre]]

def positiverate(jour,df,sex=False,rate=True):

    """

    Gives the positive rate for male and female or together
    
    Parameters
    ----------
    :param jour: A specific day or a week ("2020-11-12","2020-S45")
    :type nom: str
    :param df:  A dataframe of positivity for a  region or  with any frequency
            with a specific age class 

    :param sex: distinct the sexes
    :type sex: bool,optional, default=False

    :param rate: make a ratio with people tested if True
    :type rate: bool,optional, default=True


    Returns
    -------
    :return: A list comparing two numbers refering to male and female
    :rtype: list 

    :Examples:
    >>> positiverate("2020-11-12",granupositvity(ignoreage(Load_incquotreg().save_as_df()),2,"reg"),sex=True)


    """

    if not sex:
        if rate:
            return df.loc[jour,]["P"]/df.loc[jour,"T"]
        else: 
            return df.loc[jour,]["P"]
    else: 
        if rate:
            return [df.loc[jour,]["P_h"]/df.loc[jour,]["T_h"],df.loc[jour,]["P_f"]/df.loc[jour,]["T_f"]]
        else: return[df.loc[jour,]["P_h"],df.loc[jour,]["P_f"]]

def comparativebarplot(jour,chiffre,df,cumulative=False):
    """

    Makes the barplot comparing the two numbers obtained by other
    functions
    
    Parameters
    ----------
    :param jour: A specific day or a week ("2020-11-12","2020-S45")
    :type nom: str
    :param df:  A dataframe of positivity for a  region or  with any frequency
            with a specific age class 

    :param chiffre: positivity "P" or "T" test or even 'pop' and now
            positiverate and incidence
    :type chiffre: str

    :param cumulative: count since the beginning
    :type rate: bool,optional, default=False


    Returns
    -------
    :return: A barplot comparing two numbers refering to male and female

    :Examples:
    >>> comparativebarplot("2020-11-12","incidence",granupositvity(ignoreage(Load_incquotreg().save_as_df()),2,"reg"),cumulative=False)
    """

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    sex = ['male','female']
    if cumulative:
        df=df.cumsum()
    if chiffre=="positiverate":
        positif=positiverate(jour,df,True)
    elif chiffre=="incidence":
        positif=incidencerate(jour,df,True)
    else:
        positif = compareHF(jour,chiffre,df)
    ax.bar(sex,positif)
    plt.show()


def incidencerate(jour,df,sex=False):

    """

    Give the incidence rate (1/100 000) for a certain population
    
    Parameters
    ----------
    :param jour: A specific day or a week ("2020-11-12","2020-S45")
    :type nom: str
    :param df:  A dataframe of positivity for a  region or  with any frequency
            with a specific age class 

    :param sex: positivity "P" or "T" test or even 'pop' and now
            positiverate and incidence
    :type sex: bool,optional, default=False



    Returns
    -------
    :return: A list of with the incidence

    :Examples:
    >>> incidencerate("2020-11-12",granupositvity(ignoreage(Load_incquotreg().save_as_df()),2,"reg"),sex=True)
    """

    if not sex:
        return df.loc[jour,]["P"]*100000/df.loc[jour,"pop"]
    else: return [df.loc[jour,]["P_h"]*100000/df.loc[jour,]["pop_h"],df.loc[jour,]["P_f"]*100000/df.loc[jour,]["pop_f"]]


def barplotscomparison(jour,chiffre,granu,numero,cumulative=False,weekday="jour"):
    """

    Give different barplots by loading the correct dataset
    
    Parameters
    ----------
    :param jour: A specific day or a week ("2020-11-12","2020-S45")
    :type jour: str
    :param df:  A dataframe of positivity 

    :param granu: the granularity region, departments, country
    :type granu: str

    :param numero: the code of the region, departments, country

    :param cumulative: Since the beginning or not
    :type cumulative: bool,optional,default=False


    Returns
    -------
    :return: A list of with the incidence

    :Examples:
    >>> incidencerate("2020-11-12",granupositvity(ignoreage(Load_incquotreg().save_as_df()),2,"reg"),sex=True)
    """
    if granu=="reg":
        if weekday=="jour":
            if chiffre=="incidence":
                df=ignoreage(Load_incquotreg().save_as_df(),weekday)
            else:
                df=ignoreage(Load_posquotreg().save_as_df(),weekday)
        elif weekday=="week":
            
            if chiffre=="incidence":
                df=ignoreage(Load_inchebreg().save_as_df(),weekday)
            else:
                df=ignoreage(Load_poshebreg().save_as_df(),weekday)

    if granu=="dep":
        if weekday=="jour":
            if chiffre=="incidence":
                df=ignoreage(Load_incquotdep().save_as_df(),weekday)
            else:
                df=ignoreage(Load_posquotdep().save_as_df(),weekday)
        elif weekday=="week":
            
            if chiffre=="incidence":
                df=ignoreage(Load_inchebdep().save_as_df(),weekday)
            else:
                df=ignoreage(Load_poshebdep().save_as_df(),weekday)
    df=granupositivity(df,numero,granu)

    if chiffre in ["hosp","rea","rad","dc"]:
    
        dfhopsex=Load_hopsex().save_as_df()
        dfhopsex.index=pd.to_datetime(dfhopsex['jour'])
        del dfhopsex['jour']
        df=granupositivity(dfhopsex,numero,granu)
    comparativebarplot(jour ,chiffre,df,True)


#barplotscomparison("2020-10-12","incidence","reg",2)
#dfhopsex=Load_hopsex().save_as_df()
#dfhopsex.index=pd.to_datetime(dfhopsex['jour'])

#df=granupositivity(dfhopsex,"02","dep")

#df=df.loc["2020-10-12",]
#df

#df.loc[df["sexe"]==1]["hosp"]

#dfhopsex.index=pd.to_datetime(dfhopsex['jour'])
#dfhopsex.loc[dfhopsex['sexe']==0]["hosp"]

# %%
#dfincregrea=Load_incregrea().save_as_df()
#dfincregrea
#dfincregrea.loc[dfincregrea["numReg"]==84,:]
# %%
#dfhopdep=Load_hopdep().save_as_df()
#dfhopdep.loc[dfhopdep["dep"]=="03",:]
#%%

# %%

# %%
