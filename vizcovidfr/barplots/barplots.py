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
    if not chiffre in ["hosp","rea","rad","dc"]:

        return [df.loc[jour,][chiffre+"_h"],df.loc[jour,][chiffre+"_f"]]
    else: return [df.loc[jour,].loc[sexe==1,][chiffre],df.loc[jour,].loc[sexe==2,][chiffre]]

def positiverate(jour,df,sex=False,rate=True):
    if not sex:
        if rate:
            return df.loc[jour,]["P"]/df.loc[jour,"T"]
        else: 
            return df.loc[jour,]["P"]
    else: return [df.loc[jour,]["P_h"]/df.loc[jour,]["T_h"],df.loc[jour,]["P_f"]/df.loc[jour,]["T_f"]]


def comparativebarplot(jour,chiffre,df,cumulative=False):
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
    if not sex:
        return df.loc[jour,]["P"]*100000/df.loc[jour,"pop"]
    else: return [df.loc[jour,]["P_h"]*100000/df.loc[jour,]["pop_h"],df.loc[jour,]["P_f"]*100000/df.loc[jour,]["pop_f"]]


def barplotscomparison(jour,chiffre,granu,numero=None,cumulative=False,weekday="jour"):
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

    df=granupositivity(df,numero,granu)
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
    if chiffre in ["hosp","rea","rad","dc"]:
    
        dfhopsex=Load_hopsex().save_as_df()
        dfhopsex.index=pd.to_datetime(dfhopsex['jour'])
        del dfhopsex['jour']
        granupositivity(dfhopsex,numero,granu)

    comparativebarplot(jour ,chiffre,df,True)



barplotscomparison("2020-10-12","P","reg",2)


# %%
dfincregrea=Load_incregrea().save_as_df()
dfincregrea
dfincregrea.loc[dfincregrea["numReg"]==84,:]
# %%
dfhopdep=Load_hopdep().save_as_df()
dfhopdep.loc[dfhopdep["dep"]=="03",:]
#%%
dfhopage=Load_hopage().save_as_df()
ignoreage(dfhopage.loc[dfhopage["reg"]==1,:])

# %%

# %%
