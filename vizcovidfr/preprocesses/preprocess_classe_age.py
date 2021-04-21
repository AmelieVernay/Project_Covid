import pandas as pd
import numpy as np
from vizcovidfr.loads import load_datasets
from sklearn.linear_model import LinearRegression
model = LinearRegression()
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import operator

T = load_datasets.Load_classe_age().save_as_df()

def drop0(T):
    T = T.drop(T[T['cl_age90'] == 0].index)
    return T

def date_time(df):
    df['jour'] = pd.to_datetime(df['jour'])
    return df

def reg(x, T):
    A = T[T['reg'] == x]
    return A

def covid_day_fct(T):
    A = T.groupby(by=['jour']).sum()
    A['jour'] = A.index
    return A

def rad_dc(T):
    T1 = T[T['cl_age90'] == 0]
    X = T1.tail(18)
    return X

def rename_cl(T):
    T['cl_age90'] = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '+90']
    return T

#Creation of some dictionnaries
def dico_column(T):
    dico_col = {}
    for i in np.arange(1,T.shape[1]-2):
        dico_col[i] = T.columns[i+2]
    return dico_col

def dico_day(T):
    dico_day = {}
    for i in np.arange(0,T.shape[0]):
        dico_day[i] = T.iloc[i,9]
    return dico_day

def dico_var():
    dico_var = {'hosp':'Hospitalization', 'rea':'Reanimation', 'cl_age90':'Age', 'HospConv':'Conventional hospitalization', 'SSR_USLD':'SSR and USLD', 'autres':'Others', 'rad':'Come back home', 'dc':'Deaths'}
    return dico_var

def dico_reg():
    dico_reg = {1:'Guadeloupe', 2:'Martinique', 3:'Guyane', 4:'La Reunion', 6:'Mayotte', 11:'Île-de-France', 24:'Centre-Val de Loire', 27:'Bourgogne-Franche-Comte', 28:'Normmandie', 32:'Hauts-de-France', 44:'Grand Est', 52:'Pays de la Loire', 53:'Bretagne', 75:'Nouvelle-Aquitaine', 76:'Occitanie', 84:'Auvergne-Rhône-Alpes', 93:"Provence-Alpes Côte d'Azur", 94:'Corse'}
    return dico_reg

#Function which list the mean squared error and predict y
def degreeChoice (x,y,degree):
    #Generate a new feature matrix consisting of all polynomial combinations of the features with degree less than or equal to the specified degree. 
    polynomial_features = PolynomialFeatures(degree=degree)
    #Scaling and fitting
    x_poly = polynomial_features.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    #Prediction of y
    y_poly_pred = model.predict(x_poly)
    #Root of mean squared error (RMSE)
    rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x,y_poly_pred), key=sort_axis)
    x_p, y_poly_pred_P = zip(*sorted_zip)
    return rmse, x_p, y_poly_pred_P

def rmse_list(x, y):
    rmselist = np.zeros(100)
    x_p_list = [None]*100
    y_poly_pred_P_list=[None]*100
    for i in np.arange(1, 101):
        rmselist[i-1] ,x_p_list[i-1],y_poly_pred_P_list[i-1] = degreeChoice(x,y,i)
    return rmselist, x_p_list, y_poly_pred_P_list

