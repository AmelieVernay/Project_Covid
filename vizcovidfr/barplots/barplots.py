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

dfposfr=ignoreage(Load_posquotfr().save_as_df())

dfposfr["P_f"]
dfposfr.loc["2020-05-13"]
#dfposfr['P']/dfposfr["T"]
dfposfr

#%%
def compareHF(jour,chiffre,df):
    return [df.loc[jour,][chiffre+"_h"],df.loc[jour,][chiffre+"_f"]]

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

comparativebarplot("2020-05-14","P",dfposfr)
comparativebarplot("2020-05-15","P",dfposfr,True)

comparativebarplot("2020-06-15","positiverate",dfposfr)

#%%
dfposreg=ignoreage(Load_posquotreg().save_as_df())


granupositivity(dfposreg,2,"reg")
comparativebarplot("2020-06-15","P",granupositivity(dfposreg,2,"reg"),True)
granupositivity(dfposreg,2,"reg")
#dfposreg
#%%
dfposdep=ignoreage(Load_posquotdep().save_as_df())
dfposdep.head()
dfposdep
positiverate("2020-11-13",granupositivity(dfposdep,"03","dep"))
#granupositivity(dfposdep,"03","dep")
#%%
dfposdepheb=ignoreage(Load_poshebdep().save_as_df(),"week")
dfposdepheb
positiverate("2020-S21",granupositivity(dfposdepheb,"03","dep"))


#%%
dfposregheb=ignoreage(Load_poshebreg().save_as_df(),"week")
dfposregheb
comparativebarplot("2020-S22","P",granupositivity(dfposregheb,2,"reg"),True)
dfposregheb
#%%
dfposfrheb=ignoreage(Load_poshebfr().save_as_df(),"week")
dfposfrheb
comparativebarplot("2020-S23","T",dfposfrheb)

#%%
dfincdep=ignoreage(Load_incquotdep().save_as_df())
dfincdep
granupositivity(dfincdep,"01","dep")["P"]*100000/granupositivity(dfincdep,"01","dep")["pop"]
#%%
dfincreg=ignoreage(Load_incquotreg().save_as_df())
dfincreg
def incidencerate(jour,df,sex=False):
    if not sex:
        return df.loc[jour,]["P"]*100000/df.loc[jour,"pop"]
    else: return [df.loc[jour,]["P_h"]*100000/df.loc[jour,]["pop_h"],df.loc[jour,]["P_f"]*100000/df.loc[jour,]["pop_f"]]
comparativebarplot("2021-01-15","incidence",granupositivity(dfincreg,2,"reg"))
incidencerate("2021-01-15",granupositivity(dfincreg,3,"reg"),sex=True)


#%%
dfincfr=ignoreage(Load_incquotfr().save_as_df())
dfincfr
incidencerate("2021-01-15",dfincfr,sex=True)

#%%
dfincdepheb=ignoreage(Load_inchebdep().save_as_df(),"week")
dfincdepheb

granupositivity(dfincdepheb,"01","dep")["P"]*100000/granupositivity(dfincdepheb,"01","dep")["pop"]


#%%
dfincregheb=ignoreage(Load_inchebreg().save_as_df(),"week")
dfincregheb
comparativebarplot("2020-S50","incidence",granupositivity(dfincregheb,2,"reg"))
incidencerate("2020-S50",granupositivity(dfincregheb,2,"reg"),sex=True)
dfincregheb
granupositivity(dfincregheb,2,"reg")
#%%

dfincfrheb=ignoreage(Load_inchebfr().save_as_df(),"week")
dfincfrheb
incidencerate("2021-S01",dfincfrheb,sex=True)
comparativebarplot("2021-S01","incidence",dfincfrheb)


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
dfhopsex=Load_hopsex().save_as_df()
dfhopsex
dfhopsex.index=pd.to_datetime(dfhopsex['jour'])
del dfhopsex['jour']
dfhopsex
granupositivity(dfhopsex,"01","dep")

# %%
