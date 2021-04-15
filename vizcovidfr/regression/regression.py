#%%
import csv
from download import download
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
model = LinearRegression()

#Importation du CSV
url =  "https://www.data.gouv.fr/fr/datasets/r/08c18e08-6780-452d-9b8c-ae244ad529b3"
path_target = "./classe_age.csv"
download(url, path_target, replace = True)

T = pd.read_csv("classe_age.csv", sep=';')

#%%
#Classe 0 outliers
T = T.drop(T[T['cl_age90'] == 0].index)
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
T
#%%
R = reg(1)
R = date_time(R)
covid_jour = R.groupby(by=['jour']).sum()
covid_jour['jour'] = covid_jour.index
covid_jour
#%%
T

#%%
#Creation of some dictionnaries
dico = {'hosp':'Hospitalization', 'rea':'Reanimation', 'cl_age90':'Age', 'HospConv':'Conventional hospitalization', 'SSR_USLD':'SSR and USLD', 'rad':'Come back home', 'dc':'Deaths'}

dico_col = {}
for i in np.arange(1,T.shape[1]-2):
    dico_col[i] = T.columns[i+2]
#%%
#Function which display the scatter plot of the evolution of y in the region number num_reg
def scatter_reg(num_var, num_reg):
    #Extracting chosen region
    R = reg(num_reg)
    #Converting to datetime format
    R = date_time(R)
    #Grouping by date
    covid_jour = R.groupby(by=['jour']).sum()
    covid_jour['jour'] = covid_jour.index
    #Creating dictionnary for days
    dico_jour = {}
    for i in np.arange(0,covid_jour.shape[0]):
        dico_jour[i] = covid_jour.iloc[i,9]
    #Scatter plot
    fig = px.scatter(
    covid_jour, x=covid_jour.index, y=dico_col[num_var], opacity=0.65, trendline_color_override='darkblue', labels = {dico_col[num_var]:dico[dico_col[num_var]]}, title="Scatter plot of the evolution of" + " " + dico[dico_col[num_var]])
    fig.show()
#Examples
scatter_reg(7,1)
scatter_reg(1,94)

#%%
x = covid_jour.index
y = covid_jour['hosp']
x = x[:, np.newaxis]
y = y[:, np.newaxis]
dico_jour = {}
for i in np.arange(0,covid_jour.shape[0]):
    dico_jour[i] = covid_jour.iloc[i,9]
covid_jour = covid_jour.reset_index(drop=True)
#%%
import operator
#Function which list the mean squared error and predict y
def degreeChoice (x,y,degree):
    #Generate a new feature matrix consisting of all polynomial combinations of the features with degree less than or equal to the specified degree. 
    polynomial_features= PolynomialFeatures(degree=degree)
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
#%%
def test(a,b):
    rmselist = np.zeros(100)
    x_p_list = [None]*100
    y_poly_pred_P_list=[None]*100
    for i in np.arange(1, 101):
        rmselist[i-1] ,x_p_list[i-1],y_poly_pred_P_list[i-1] = degreeChoice(a,b,i)
        return rmselist
test(x,y)
#%%
list(rmselist).index(rmselist.min())
#%%
def poly_fit(num_var, num_reg):
    R = reg(num_reg)
    R = date_time(R)
    covid_jour = R.groupby(by=['jour']).sum()
    covid_jour['jour'] = covid_jour.index
    x = covid_jour.index
    y = covid_jour[dico_col[num_var]]
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    dico_jour = {}
    for i in np.arange(0,covid_jour.shape[0]):
        dico_jour[i] = covid_jour.iloc[i,9]
    covid_jour = covid_jour.reset_index(drop=True)
#%%
    #Listing RMSE
    rmselist = np.zeros(100)
    x_p_list = [None]*100
    y_poly_pred_P_list=[None]*100
    for i in np.arange(1, 101):
        rmselist[i-1] ,x_p_list[i-1],y_poly_pred_P_list[i-1] = degreeChoice(x,y,i)
    #Degree of polynomial regression
    deg = list(rmselist).index(rmselist.min())
    return deg
poly_fit(1,1)
#%%
    fig = plt.scatter(dico_jour.values(), y)
    plt.plot(dico_jour.values(),y_poly_pred_P_list[deg],color='r')
    plt.title("Polynomial regression of" + " " + dico[dico_col[num_var]]).set_fontsize(20)
    blue_line = mlines.Line2D([], [], color='blue',
                          markersize=15,
                          marker='.', label=dico[dico_col[num_var]])
    red_line = mlines.Line2D([], [], color='red',
                          markersize=15, label='Regression curve')
    plt.legend(handles=[blue_line, red_line])
    plt.figtext(0.15, 0.85, f'Degree of polynomial regression : {deg}', fontsize=16)
    plt.show()
poly_fit(1,1)
#%%
R = reg(1)
R = date_time(R)
R
# %%
covid_jour1 = R.groupby(by=['jour']).sum()
covid_jour1
#%%
covid_jour1['jour'] = covid_jour1.index
covid_jour1
#%%
dico_jour = {}
for i in np.arange(0,covid_jour.shape[0]):
    dico_jour[i] = covid_jour1.iloc[i,9]
dico_jour
#%%
covid_jour1 = covid_jour1.reset_index(drop=True)
covid_jour1

rmselist = np.zeros(100)
x_p_list = [None]*100
y_poly_pred_P_list=[None]*100
for i in np.arange(1, 101):
    rmselist[i-1] ,x_p_list[i-1],y_poly_pred_P_list[i-1] = degreeChoice (x,y,i)
     
plt.plot(np.arange(1, 101), rmselist, color='r')
plt.show()
#%%
y_poly_pred_P[6]
#%%
x

#%%
from sklearn.pipeline import make_pipeline
polyreg = make_pipeline(PolynomialFeatures(7),LinearRegression())
polyreg.fit(x,y)

#%%
plt.scatter(x,y)
plt.plot(dico_jour.values(),polyreg.predict(x),color="black")
plt.title("Polynomial regression with degree "+str(7))
plt.show()
#%%
coefs = np.polyfit(np.arange(393), y, 7)
plt.figure()
plt.plot(np.arange(450), np.polyval(coefs, np.arange(450)), color="black")
plt.title("Polyfit degree "+str(7))
plt.scatter(x,y)
plt.show()
#%%
coefs

import matplotlib.lines as mlines
fig = plt.scatter(dico_jour.values(), y)

#degre 7
P = plt.plot(dico_jour.values(),y_poly_pred_P_list[6],color='r')
plt.title('Regression polynomiale deg 7')
plt.title('Regression polynomiale deg 7').set_fontsize(20)
blue_line = mlines.Line2D([], [], color='blue',
                          markersize=15,
                          marker='.', label='Regression curve')
red_line = mlines.Line2D([], [], color='red',
                          markersize=15, label='Regression curve')
plt.legend(handles=[blue_line, red_line])
plt.figtext(0.15, 0.85, 'Degree of polynomial regression : 7', fontsize=16)

#%%
#R2 prediction
r2_score(y,y_poly_pred_P_list[6])



