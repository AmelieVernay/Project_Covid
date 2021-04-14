#%%
from download import download
import pandas as pd
import seaborn as sns
#%%
urlposfr="https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c"
pathtarget="../data/posquotfr.csv"
download(urlposfr,pathtarget,replace=True)
dfposfr=pd.read_csv(pathtarget,sep=";")
#dfposfr
#dfposfr['jour'] = pd.to_datetime(dfposfr['jour'])
#dfposfr= dfposfr.set_index('jour')#,'cl_age90'
#dfposfr["incid"]=dfposfr["P"]/dfposfr['pop']*100000
#dfposfr=dfposfr['2020-11'][['incid','cl_age90']].reset_index()
#dfposfr['jour']=pd.to_datetime(dfposfr['jour']).dt.date
#dfposfr.drop(dfposfr.loc[dfposfr["cl_age90"]==0].index,inplace=True)

#ax=sns.heatmap(dfposfr.pivot("jour","cl_age90","incid"))
def heatmapage(df,debut,fin=None):

    df['jour'] = pd.to_datetime(df['jour'])
    df= df.set_index('jour')#,'cl_age90'
    df["incid"]=df["P"]/df['pop']*100000
    if fin is None:
        df=df[debut][['incid','cl_age90']].reset_index()
    else:
        df=df[debut:fin][['incid','cl_age90']].reset_index()
    df['jour']=pd.to_datetime(df['jour']).dt.date
    df.drop(df.loc[df["cl_age90"]==0].index,inplace=True)
    ax=sns.heatmap(df.pivot("jour","cl_age90","incid"))

def grantable(df,granularite,nom):
    return df.loc[df[granularite]==nom]

heatmapage(dfposfr,"2020-11")

# %%
urlposreg="https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
pathtarget="../data/posquotreg.csv"
download(urlposreg,pathtarget,replace=True)
dfposreg=pd.read_csv(pathtarget,sep=";")
heatmapage(grantable(dfposreg,"reg",1),"2020-11")
#%%
urlposreg="https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
pathtarget="../data/posquotreg.csv"
download(urlposreg,pathtarget,replace=True)
dfposreg=pd.read_csv(pathtarget,sep=";")
dfposreg=dfposreg.loc[dfposreg["jour"]=="2020-11-06"]
dfposreg["incid"]=dfposreg["P"]/dfposreg['pop']*100000
dfposreg.drop(dfposreg.loc[dfposreg["cl_age90"]==0].index,inplace=True)
dfposreg
ax=sns.heatmap(dfposreg.pivot("reg","cl_age90","incid"))
# %%
urlposreg="https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
pathtarget="../data/posquotreg.csv"
download(urlposreg,pathtarget,replace=True)
dfposreg=pd.read_csv(pathtarget,sep=";")
dfposreg["incid"]=dfposreg["P"]/dfposreg['pop']*100000
dfposreg
dfposreg=dfposreg.loc[dfposreg["cl_age90"]==0]
dfposreg['jour'] = pd.to_datetime(dfposreg['jour'])
dfposreg= dfposreg.set_index('jour')#,'cl_age90'
dfposreg=dfposreg["2020-11"][['incid',"reg",'cl_age90']].reset_index()
dfposreg['jour']=pd.to_datetime(dfposreg['jour']).dt.date
dfposreg
ax=sns.heatmap(dfposreg.pivot("jour","reg","incid"))




# %%
