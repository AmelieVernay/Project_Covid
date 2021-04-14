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
T = T.drop(T[T['cl_age90'] == 0].index)
T
#%%
T['cl_age90'] = T['cl_age90'] - 9
T
#%%
T

#%%
def reg(x):
    A = T[T['reg'] == x]
    return A
reg(1)

#%%
T
#%%
def date_time(df):
    df['jour'] = pd.to_datetime(df['jour'])
    return df
T = date_time(T)

#%%
def ols(x):
    T = T.drop(T[T['cl_age90'] == 0].index)
    T = date_time(T)
    covid_jour = T.groupby(by=['jour']).sum()
    fig = px.scatter(
    covid_jour, x=covid_jour.index, y='hosp', opacity=0.65,
    trendline='ols', trendline_color_override='darkblue'
)
fig.show()
#%%
T
#%%
fig = px.scatter(
    reg(1,10), x='jour', y='hosp', opacity=0.65,
    trendline='ols', trendline_color_override='darkblue'
)
fig.show()

#%%
reg(1)
#%%
R = reg(1)
R = date_time(R)
R
# %%
covid_jour = R.groupby(by=['jour']).sum()
covid_jour
#%%
fig = px.scatter(
    covid_jour, x=covid_jour.index, y='hosp', opacity=0.65,
    trendline='ols', trendline_color_override='darkblue'
)
fig.show()

# %%
covid_age = R.groupby(by=['cl_age90']).sum()
covid_age

#%%
fig = px.scatter(
    covid_age, x=covid_age.index, y='hosp', opacity=0.65,
    trendline='ols', trendline_color_override='darkblue'
)
fig.show()
# %%
