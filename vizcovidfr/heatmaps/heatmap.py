#%%
from download import download
import pandas as pd
import seaborn as sns
from vizcovidfr.loads.load_datasets import Load_posquotfr,Load_posquotreg,Load_posquotdep
from vizcovidfr.loads.load_datasets import Load_poshebreg,Load_poshebfr,Load_incregrea

from vizcovidfr.preprocesses.preprocess_positivity import granupositivity
#%%
def S2020_2021(semaine):
    return int(semaine[3])*53+int(semaine[6:8])

def W2020_2021(number):
    if number==53:
        return "202"+str(number//54)+f"-S{number:02}"
    return "202"+str(number//54)+f"-S{number%53:02}"
#%%
dfposfr=Load_posquotfr().save_as_df()
def heatmapageday(df,debut,fin=None,weekday="jour"):

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


heatmapageday(dfposfr,"2020-11")

# %%
dfposreg=Load_posquotreg().save_as_df()
heatmapageday(granupositivity(dfposreg,1,"reg"),"2020-11")
granupositivity(dfposreg,1,"reg")
#%%
dfposreg=Load_posquotreg().save_as_df()
def heatmapregage(df,granu,weekday):
    if len(weekday)>8:
        df=df.loc[df["jour"]==weekday]
    else:
        df=df.loc[df["week"]==weekday]
    df["incid"]=df["P"]/df['pop']*100000
    df.drop(df.loc[df["cl_age90"]==0].index,inplace=True)
    sns.heatmap(df.pivot(granu,"cl_age90","incid"))

heatmapregage(dfposreg,"2020-11-06","reg")


# %%


dfposreg=Load_posquotreg().save_as_df()
def heatmapregday(df,age,debut,granu="reg",weekday="jour",fin=None):
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

heatmapregday(dfposreg,0,"2020-11")
# %%
#dfposdep=Load_posquotdep().save_as_df()
#heatmapregday(dfposdep,0,"dep","2020-11")
#heatmapregage(dfposdep,"2020-11-06","dep")


# %%
dfposhebreg=Load_poshebreg().save_as_df()
dfposhebreg
# %%

    
W2020_2021(13)

debut="2020-S36"
fin="2021-S02"
heatmapregday(dfposhebreg,0,debut="2020-S36",fin="2021-S02",weekday="week")

heatmapregage(dfposhebreg,"reg","2020-S38")
# %%
dfincregrea=Load_incregrea().save_as_df()
dfincregrea
dfincregrea["jour"] = pd.to_datetime(dfincregrea["jour"])
dfincregrea= dfincregrea.set_index('jour')
dfincregrea=dfincregrea["2020-11"].reset_index()
dfincregrea["jour"] = pd.to_datetime(dfincregrea['jour']).dt.date

sns.heatmap(dfincregrea.pivot("jour","numReg","incid_rea"))



