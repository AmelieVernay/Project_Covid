#%%
import csv
from download import download
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact

#Importation du CSV
url2 = 'https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv'
url = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
path_target = "./chiffres-cles.csv"
download(url, path_target, replace = True)

T = pd.read_csv("chiffres-cles.csv", sep=',')
print(T)
T.columns

# %%
#Suppression des 4 dernières colonnes
data = T.drop(columns=['source_nom', 'source_url', 'source_archive', 'source_type'])
data


# %%
data.columns = ['Date', 'Granularite', 'Maille code', 'Maille nom', 'Cas confirmés', 'Cas EHPAD', 'Cas confirmés EHPAD', 'Cas possibles EHPAD', 'Deces', 'Deces EHPAD','reanimation', 'hospitalises',
       'Nouvelles hospitalisations', 'Nouvelles reanimations', 'Gueris', 'Depistes']
data
# %%
data_reg = data[data['Granularite'] == 'region']
data_reg
# %%
covid_today = data_reg.groupby(by='Maille nom').sum()
covid_today
# %%
plt.hist(covid_today.index, bins=255)
plt.show()
# %%
covid_today['Cas confirmés'].hist()

# %%
