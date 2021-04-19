#%%
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
model = LinearRegression()
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_classe_age as pca

T = load_datasets.Load_classe_age().save_as_df()

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
#Function which display the scatter plot of the evolution of y in the region number num_reg
def scatter_reg(num_var, num_reg):
    #Extracting chosen region
    T2 = pca.reg(num_reg, T)
    #Converting to datetime format
    T2 = pca.date_time(T2)
    dico_col = pca.dico_column(T2)
    #Grouping by date
    covid_day = pca.covid_day_fct(T2)
    #Creating dictionnaries
    #dico_day = pca.dico_day(covid_day)
    dico_reg = pca.dico_reg()
    dico_var = pca.dico_var()
    #Scatter plot
    fig = px.scatter(
    covid_day, x=covid_day.index, y=dico_col[num_var], opacity=0.65, trendline_color_override='darkblue', labels = {dico_col[num_var]:dico_var[dico_col[num_var]], 'index':'Date'}, title="Scatter plot of the evolution of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg])
    fig.show()
#Examples
scatter_reg(6,6)
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
#x = np.arange(0,covid_jour.shape[0])
#x = x[:, np.newaxis]
import operator
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

#%%
list(rmselist).index(rmselist.min())
#%%
def poly_fit(num_var, num_reg):
    R = pca.reg(num_reg, T)
    R = pca.date_time(R)
    dico_col = pca.dico_column(R)
    covid_day = pca.covid_day_fct(R)
    x = np.arange(0,covid_day.shape[0])
    y = covid_day[dico_col[num_var]]
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    dico_days = pca.dico_day(covid_day)
    dico_var = pca.dico_var()
    dico_reg = pca.dico_reg()
    covid_day = covid_day.reset_index(drop=True)
    #Listing RMSE
    #rmselist = np.zeros(100)
    #x_p_list = [None]*100
    #y_poly_pred_P_list=[None]*100
    #for i in np.arange(1, 101):
     #   rmselist[i-1] ,x_p_list[i-1],y_poly_pred_P_list[i-1] = pca.degreeChoice(x,y,i)
    rmselist, x_p_list, y_poly_pred_P_list = pca.rmse(x, y)
    #Degree of polynomial regression
    deg = list(rmselist).index(rmselist.min())
    fig = plt.scatter(dico_days.values(), y)
    plt.plot(dico_days.values(),y_poly_pred_P_list[deg],color='r')
    plt.suptitle("Polynomial regression of" + " " + dico_var[dico_col[num_var]] + " in " + dico_reg[num_reg]).set_fontsize(15)
    blue_line = mlines.Line2D([], [], color='blue',
                          markersize=15,
                          marker='.', label=dico_var[dico_col[num_var]])
    red_line = mlines.Line2D([], [], color='red',
                          markersize=15, label='Regression curve')
    plt.legend(handles=[blue_line, red_line])
    plt.title(f'Degree of polynomial regression : {deg+1}', fontsize=10)
    plt.show()
poly_fit(7,94)
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
R = pca.reg(1, T)
R = pca.date_time(R)
dico_col = pca.dico_column(R)
covid_day = pca.covid_day(R)
x = np.arange(0,covid_day.shape[0])
y = covid_day[dico_col[1]]
x = x[:, np.newaxis]
y = y[:, np.newaxis]
dico_days = pca.dico_day(covid_day)
dico_var = pca.dico_var()
dico_reg = pca.dico_reg()
covid_day = covid_day.reset_index(drop=True)
#Listing RMSE
rmselist = np.zeros(100)
x_p_list = [None]*100
y_poly_pred_P_list=[None]*100
for i in np.arange(1, 101):
    rmselist[i-1] ,x_p_list[i-1],y_poly_pred_P_list[i-1] = degreeChoice(x,y,i)

#%%
from sklearn.metrics import r2_score
r2_score(y,y_poly_pred_P_list[6])

#%%
A = poly_fit(1,1)
# %%
def R2(num_var, num_reg):
    P = poly_fit(num_var, num_reg)
