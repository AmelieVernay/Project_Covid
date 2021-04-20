import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_classe_age as pca

T = load_datasets.Load_classe_age().save_as_df()

def hist_age(num_var, num_reg):
    #T = load_datasets.Load_classe_age().save_as_df()
    T2 = pca.drop0(T)
    data_reg = pca.reg(num_reg, T2)
    dico_col = pca.dico_column(data_reg)
    data_reg_age = data_reg.groupby(by='cl_age90').sum()
    data_reg_age['cl_age90'] = data_reg_age.index
    data_reg_age['cl_age90'] = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '+90']
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    fig = px.bar(data_reg_age, x = 'cl_age90', y = dico_col[num_var], 
                hover_data = [dico_col[num_var]],
                color = dico_col[num_var],
                labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'cl_age90':'Age'},
                height = 400,
                title="Bar plot of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg] + " by age group today")
    fig.show()
