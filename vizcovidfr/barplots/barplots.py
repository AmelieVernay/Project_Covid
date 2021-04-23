# ---------- requirements ----------
from download import download
import pandas as pd
import time

# local reqs
from vizcovidfr.loads.load_datasets import Load_posquotfr,Load_posquotreg,Load_posquotdep
from vizcovidfr.loads.load_datasets import Load_poshebdep,Load_poshebreg,Load_poshebfr
from vizcovidfr.loads.load_datasets import Load_incquotdep,Load_incquotreg,Load_incquotfr
from vizcovidfr.loads.load_datasets import Load_inchebdep,Load_inchebreg,Load_inchebfr
from vizcovidfr.loads.load_datasets import Load_incregrea,Load_hopdep,Load_hopage,Load_hopsex
from vizcovidfr.preprocesses.preprocess_positivity import ignoreage,granupositivity


#dfposfr=ignoreage(Load_posquotfr().save_as_df())

#dfposfr["P_f"]
#dfposfr.loc["2020-05-13"]
#dfposfr['P']/dfposfr["T"]
#dfposfr


def compareHF(jour,chiffre,granu,number=None,cumulative=False):
    
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
    start = time.time()
    if chiffre in  ["P","T","positvity"]:
        if granu=="France":
            if len(jour)>8:
                df=ignoreage(Load_posquotfr().save_as_df())
            else:
                df=ignoreage(Load_poshebfr().save_as_df())
        elif granu=="reg":
            if len(jour)>8:
                df=ignoreage(Load_posquotreg().save_as_df())
            else:
                df=ignoreage(Load_poshebreg().save_as_df())
        if granu =="reg":
            df=granupositivity(df,number,granu)
    if chiffre == "incidence":
        if granu=="France":
            if len(jour)>8:
                df=ignoreage(Load_incquotfr().save_as_df())
            else:
                df=ignoreage(Load_inchebfr().save_as_df())
        elif granu=="reg":
            if len(jour)>8:
                df=ignoreage(Load_incquotreg().save_as_df())
            else:
                df=ignoreage(Load_inchebreg().save_as_df())
        if granu =="reg":
            df=granupositivity(df,number,granu)

    
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    sex = ['male','female']
    if cumulative:
        df=df.cumsum()
    if chiffre in  ["P","T"]:
        positive= [df.loc[jour,][chiffre+"_h"],df.loc[jour,][chiffre+"_f"]]
    if chiffre =="positivity":
        positive= [df.loc[jour,]["P_h"]/df.loc[jour,]["T_h"],df.loc[jour,]["P_f"]/df.loc[jour,]["T_f"]]
    if chiffre== "incidence":
         positive= [df.loc[jour,]["P_h"]*100000/df.loc[jour,]["pop_h"],df.loc[jour,]["P_f"]*100000/df.loc[jour,]["pop_f"]]
    ax.bar(sex,positive)
    plt.show()

    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))



compareHF("2020-11-12","incidence",granu="France")
