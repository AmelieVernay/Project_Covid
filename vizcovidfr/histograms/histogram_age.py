#%%
import csv
from download import download
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Importation du CSV
url =  "https://www.data.gouv.fr/fr/datasets/r/08c18e08-6780-452d-9b8c-ae244ad529b3"
path_target = "./classe_age.csv"
download(url, path_target, replace = True)

T = pd.read_csv("classe_age.csv", sep=';')


#%%
dico = {'hosp':'Hospitalization', 'rea':'Reanimation', 'cl_age90':'Age', 'HospConv':'Conventional hospitalization', 'SSR_USLD':'SSR and USLD', 'rad':'Come back home', 'dc':'Deaths'}

def hist_age(num_var, num_reg):
    data_reg = T[T['reg'] == num_reg]
    data_reg_age = data_reg.groupby(by='cl_age90').sum()
    dico_col = {}
    for i in np.arange(1,data_reg_age.shape[1]):
        dico_col[i] = data_reg_age.columns[i]
    data_reg_age.drop(0, inplace=True)
    data_reg_age['cl_age90'] = data_reg_age.index
    data_reg_age['cl_age90'] = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '+90']
    fig = px.bar(data_reg_age, x = 'cl_age90', y = dico_col[num_var], 
                hover_data = [dico_col[num_var]],
                color = dico_col[num_var],
                labels = {dico_col[num_var]:dico[dico_col[num_var]], 'cl_age90':'Age'},
                height = 400,
                title="Bar plot of" + " " + dico[dico_col[num_var]] + " by age group")
    fig.show()

#%%
hist_age(7,1)
hist_age(4,1)
hist_age(1,94)

#%%
fig = px.bar(data_reg_age, x='cl_age90', y='hosp',
             hover_data=['hosp', 'rea'], color='hosp',
             labels={'hosp':'Hospitalization', 'rea':'Reanimation','cl_age90':'Age'}, height=400)
fig.show()


