#%%
import pandas as pd
from download import download
pd.options.display.max_rows = 25
import datetime
import plotly.express as px
import numpy as np

##Vaccination part
#line chart with number of vaccinated people in the whole France




#line chart which represents the french vaccine storage per vaccine type 
#%%
url = "https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-stocks-des-doses-de-vaccins-contre-la-covid-19/#_"
path_target = "./stocks-es-national.csv"
download(url, path_target, replace=True)

#Creation of dataframe
df_Vac_type = pd.read_csv("C:/Users/quenf/OneDrive/Desktop/Semestre 2 MIND/Développement logiciel/stocks-es-national.csv")


# %%
fig = px.line(df_Vac_type, x="date", y="nb_doses", color='type_de_vaccin', title = 'Vaccine storage according to vaccine type in the whole France' )
fig.show()

#line chart with total number of vaccine doses
# %%
df2 = df_Vac_type.groupby(['date'])['nb_doses'].agg('sum') #cumules vaccine doses whatever its type per date, in a new vector

#need to change this part of the code, shorten it
df_Vac_type['Sum_per_date'] = np.zeros(24)

df_Vac_type['Sum_per_date'][0] = df2[0]
df_Vac_type['Sum_per_date'][1] = df2[0]
df_Vac_type['Sum_per_date'][2] = df2[1]
df_Vac_type['Sum_per_date'][3] = df2[1]
df_Vac_type['Sum_per_date'][4] = df2[2]
df_Vac_type['Sum_per_date'][5] = df2[2]
df_Vac_type['Sum_per_date'][6] = df2[3]
df_Vac_type['Sum_per_date'][7] = df2[3]
df_Vac_type['Sum_per_date'][8] = df2[3]
df_Vac_type['Sum_per_date'][9] = df2[4]
df_Vac_type['Sum_per_date'][10] = df2[4]
df_Vac_type['Sum_per_date'][11] = df2[4]
df_Vac_type['Sum_per_date'][12] = df2[5]
df_Vac_type['Sum_per_date'][13] = df2[5]
df_Vac_type['Sum_per_date'][14] = df2[5]
df_Vac_type['Sum_per_date'][15] = df2[6]
df_Vac_type['Sum_per_date'][16] = df2[6]
df_Vac_type['Sum_per_date'][17] = df2[6]
df_Vac_type['Sum_per_date'][18] = df2[7]
df_Vac_type['Sum_per_date'][19] = df2[7]
df_Vac_type['Sum_per_date'][20] = df2[7]
df_Vac_type['Sum_per_date'][21] = df2[8]
df_Vac_type['Sum_per_date'][22]= df2[8]
df_Vac_type['Sum_per_date'][23] = df2[8]

#%%
fig2 = px.line(df_Vac_type, x="date", y= "Sum_per_date", title = 'Vaccine storage whatever its type in the whole France')
fig2.show()


# %%
