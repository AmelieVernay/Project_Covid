#%%
from download import download
import pandas as pd
#%%

urlposfr="https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c"
pathtarget="../data/posquotfr.csv"
download(urlposfr,pathtarget,replace=True)
dfposfr=pd.read_csv(pathtarget,sep=";")
dfposfr.groupby(['jour']).sum()

P_f=dfposfr.loc[dfposfr["cl_age90"]==0]["P_f"]

P_h=dfposfr.loc[dfposfr["cl_age90"]==0]["P_h"]

T_f=dfposfr.loc[dfposfr["cl_age90"]==0]["T_f"]

T_h=dfposfr.loc[dfposfr["cl_age90"]==0]["T_h"]

P_f
dfposfr.loc[dfposfr["cl_age90"]==0].groupby(["jour"]).sum().loc["2020-05-13",]
def ignoreage(df,weekday="jour"):
    return df.loc[df['cl_age90']==0].groupby([weekday]).sum()
#%%
def compareHF(jour,chiffre,df):
    return [df.loc[jour,][chiffre+"_h"],df.loc[jour,][chiffre+"_f"]]

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

comparativebarplot("2020-05-14","P",ignoreage(dfposfr))
comparativebarplot("2020-05-15","P",ignoreage(dfposfr),True)

def positiverate(jour,df,sex=False,rate=True):
    if not sex:
        if rate:
            return df.loc[jour,]["P"]/df.loc[jour,"T"]
        else: 
            return df.loc[jour,]["P"]
    else: return [df.loc[jour,]["P_h"]/df.loc[jour,]["T_h"],df.loc[jour,]["P_f"]/df.loc[jour,]["T_f"]]
comparativebarplot("2020-06-15","positiverate",ignoreage(dfposfr))

#%%
urlposreg="https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
pathtarget="../data/posquotreg.csv"
download(urlposreg,pathtarget,replace=True)
dfposreg=pd.read_csv(pathtarget,sep=";")
dfposreg.head()
dfposreg.loc[dfposreg["reg"]==1,:]
def subtablepos(df,granularite,number,weekday="jour"):
    return ignoreage(df.loc[df[granularite]==number,:],weekday)


dfposreg.head()
dfposreg.groupby(["reg","jour"]).sum()
dfposreg.loc[dfposreg["reg"]==1,:].groupby(['jour']).sum()
subtablepos(dfposreg,"reg",2)
comparativebarplot("2020-06-15","P",subtablepos(dfposreg,"reg",2),True)
dfposreg
#%%
urlposdep="https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675"
pathtarget="../data/posquotdep.csv"
download(urlposdep,pathtarget,replace=True)
dfposdep=pd.read_csv(pathtarget,sep=";")
dfposdep.head()
dfposdep
positiverate("2020-11-13",ignoreage(dfposdep.loc[dfposdep["dep"]=="03",:]))
#%%
urlposdepheb="https://www.data.gouv.fr/fr/datasets/r/dd3ac13c-e87f-4b33-8897-07baff4e1783"
pathtarget="../data/poshebdep.csv"
download(urlposdepheb,pathtarget,replace=True)
dfposdepheb=pd.read_csv(pathtarget,sep=";")
dfposdepheb
positiverate("2020-S21",ignoreage(dfposdepheb.loc[dfposdepheb["dep"]=="03",:],"week"))


#%%
urlposregheb="https://www.data.gouv.fr/fr/datasets/r/1ff7af5f-88d6-44bd-b8b6-16308b046afc"
pathtarget="../data/poshebreg.csv"
download(urlposregheb,pathtarget,replace=True)
dfposregheb=pd.read_csv(pathtarget,sep=";")
dfposregheb
subtablepos(dfposregheb,"reg",2,"week")
comparativebarplot("2020-S22","P",subtablepos(dfposregheb,"reg",2,"week"),True)
dfposregheb
#%%
urlposfrheb="https://www.data.gouv.fr/fr/datasets/r/2f0f720d-fbd2-41a7-95b4-3a70ff5a9253"
pathtarget="../data/poshebfr.csv"
download(urlposfrheb,pathtarget,replace=True)
dfposfrheb=pd.read_csv(pathtarget,sep=";")
dfposfrheb
comparativebarplot("2020-S23","T",ignoreage(dfposfrheb,"week"))

#%%
urlincdep="https://www.data.gouv.fr/fr/datasets/r/19a91d64-3cd3-42fc-9943-d635491a4d76"
pathtarget="../data/incquotdep.csv"
download(urlincdep,pathtarget,replace=True)
dfincdep=pd.read_csv(pathtarget,sep=";")
subtablepos(dfincdep,"dep","01")["P"]*100000/subtablepos(dfincdep,"dep","01")["pop"]
#%%
urlincreg="https://www.data.gouv.fr/fr/datasets/r/ad09241e-52fa-4be8-8298-e5760b43cae2"
pathtarget="../data/incquotreg.csv"
download(urlincreg,pathtarget,replace=True)
dfincreg=pd.read_csv(pathtarget,sep=";")
dfincreg
def incidencerate(jour,df,sex=False):
    if not sex:
        return df.loc[jour,]["P"]*100000/df.loc[jour,"pop"]
    else: return [df.loc[jour,]["P_h"]*100000/df.loc[jour,]["pop_h"],df.loc[jour,]["P_f"]*100000/df.loc[jour,]["pop_f"]]
comparativebarplot("2021-01-15","incidence",subtablepos(dfincreg,"reg",2))
incidencerate("2021-01-15",subtablepos(dfincreg,"reg",3),sex=True)


#%%
urlincfr="https://www.data.gouv.fr/fr/datasets/r/57d44bd6-c9fd-424f-9a72-7834454f9e3c"
pathtarget="../data/incquotfr.csv"
download(urlincfr,pathtarget,replace=True)
dfincfr=pd.read_csv(pathtarget,sep=";")
dfincfr
incidencerate("2021-01-15",ignoreage(dfincfr),sex=True)

#%%
urlincdepheb="https://www.data.gouv.fr/fr/datasets/r/bb2a18f3-bdd5-4101-8687-945d6e4e435f"
pathtarget="../data/inchebdep.csv"
download(urlincdepheb,pathtarget,replace=True)
dfincdepheb=pd.read_csv(pathtarget,sep=";")
dfincdepheb
subtablepos(dfincdepheb,"dep","01","week")["P"]*100000/subtablepos(dfincdepheb,"dep","01","week")["pop"]


#%%
urlincregheb="https://www.data.gouv.fr/fr/datasets/r/66b09e9a-41b5-4ed6-b03c-9aef93a4b559"
pathtarget="../data/inchebreg.csv"
download(urlincregheb,pathtarget,replace=True)
dfincregheb=pd.read_csv(pathtarget,sep=";")
dfincregheb
comparativebarplot("2020-S50","incidence",subtablepos(dfincregheb,"reg",2,"week"))
incidencerate("2020-S50",subtablepos(dfincregheb,"reg",3,"week"),sex=True)
subtablepos(dfincregheb,"reg",2,"week")

#%%

urlincfrheb="https://www.data.gouv.fr/fr/datasets/r/2360f82e-4fa4-475a-bc07-9caa206d9e32"
pathtarget="../data/inchebfr.csv"
download(urlincfrheb,pathtarget,replace=True)
dfincfrheb=pd.read_csv(pathtarget,sep=";")
dfincfrheb
incidencerate("2021-S01",dfincfrheb.groupby(['week']).sum(),sex=True)
comparativebarplot("2021-S01","incidence",dfincfrheb.groupby(['week']).sum())


# %%
urlincregrea="https://www.data.gouv.fr/fr/datasets/r/a1466f7f-4ece-4158-a373-f5d4db167eb0"
pathtarget="../data/increareg.csv"
download(urlincregrea,pathtarget,replace=True)
dfincregrea=pd.read_csv(pathtarget,sep=";",encoding="latin-1")
dfincregrea
dfincregrea.loc[dfincregrea["numReg"]==84,:]
# %%
urlhopdep="https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c"
pathtarget="../data/hopdep.csv"
download(urlhopdep,pathtarget,replace=True)
dfhopdep=pd.read_csv(pathtarget,sep=";",encoding="latin-1")
dfhopdep.loc[dfhopdep["dep"]=="03",:]
#%%
urlhopage="https://www.data.gouv.fr/fr/datasets/r/08c18e08-6780-452d-9b8c-ae244ad529b3"
pathtarget="../data/hopage.csv"
download(urlhopage,pathtarget,replace=True)
dfhopage=pd.read_csv(pathtarget,sep=";",encoding="latin-1")
ignoreage(dfhopage.loc[dfhopage["reg"]==1,:])

# %%
