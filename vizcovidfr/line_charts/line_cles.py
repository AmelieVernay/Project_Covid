# ---------- requirements ----------

import pandas as pd
import matplotlib.pyplot as plt
from download import download
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from vizcovidfr.loads.load_datasets import Load_posquotdep,Load_posquotreg,Load_chiffres_fr
from vizcovidfr.preprocesses import preprocess_chiffres_cles,preprocess_positivity
from vizcovidfr.preprocesses import preprocess_positivity
from vizcovidfr.preprocesses.preprocess_positivity import REGIONS,DEPARTMENTS
import matplotlib.pyplot as plt

def keyseries(nom,chiffre,evo=True):

    """

    Extract the main time series about information concerning
    the evolution of the deases COVID-19 in France or a sub-part of France

    Parameters
    ----------
    :param nom: A name in French of a department, or region , 
        or the whole territory
    :type nom: str
    :param chiffre: The figure of interest in French suc as "deces" , "cas" 

        - 'cas_confirmes':
            number of confirmed cases
        - 'cas_ehpad':
            number of confirmed cases in 
        - 'deces':
            display the cumulated number of death due to
            the Covid-19 in France from the beginning of the pandemic, up to
            the given date
    
    :type chiffre: str

    :param evo: New per day or cumulative
    :type evo: bool, optional, default=True



    Returns
    -------
    :return: A time series until today since the beginning of the records of the figure of interest 
    :rtype: 'pandas.Series' 
    evo: New per day or cumulative

    :Examples:
    >>> keyseries("France","cas",evo=False)


    """

    fr= nom=="France"

    if chiffre in ["deces_à_l'hôpital","deceshop"]:

        chiffre="total_deces_hopital"
        fr=True #no big difference with only "deces"

    if fr:

        
        df_covid=preprocess_chiffres_cles.gooddates(Load_chiffres_fr().save_as_df())

    if chiffre in ["cas","nombre_de_cas","cas_confirmes"]:

        chiffre="cas_confirmes"

        if fr:

            chiffre="total_cas_confirmes"

    elif chiffre in ["hospitalisation","hôpital","hospitalises"]:
        
        chiffre="hospitalises"

        if fr:

            chiffre="patients_hospitalises"

    elif chiffre in ["deces_ehpad"]:

        if fr:

            chiffre="total_deces_ehpad"

    elif chiffre in ["morts"]:

        chiffre="deces"

    elif chiffre in ["reanimation"]:

        if fr:

            chiffre="patients_reanimation"

    elif chiffre in ["cas_confirmes_ehpad"]:

        if fr:

            chiffre="total_cas_confirmes_ephad"

    elif chiffre in ["gueris"]:

        if fr:

            chiffre="total_patients_gueris" #options with
            # different expressions for a same argument

    if fr:

        if evo:

            return df_covid[chiffre].diff()

        return df_covid[chiffre]

    elif chiffre in ["cas_confirmes"]: #need specific datasets

        if nom in REGIONS.keys():
            df=preprocess_positivity.granupositivity(Load_posquotreg().save_as_df(),nom)
        
        elif nom in DEPARTMENTS.keys():
            df=preprocess_positivity.granupositivity(Load_posquotdep().save_as_df(),nom)

        
        if evo:

            return df['P']

        else: 
                
            return df['P'].cumsum()





    if evo:

        return preprocess_chiffres_cles.keysubtablename(nom)[chiffre].dropna().diff()

    return preprocess_chiffres_cles.keysubtablename(nom)[chiffre].dropna()


def plotseries(series,average=True):

    """

    series: a time series
    average: do the moving average or not

    Allows you to plot a time series wih or without a moving average


    """
    sns.set(rc={'figure.figsize':(11, 4)})

    if average:

        ax=series.rolling(window=7).mean().plot()

    else:

        ax=series.plot()
    return ax

def keyplot(nom,chiffre,evo=True,average=True):

    """
    nom: A part of France
    chiffre: A figure
    average: do the moving average or not
    evo: New per day or cumulative

    Plot the time series associates with figures of Covid-19.
    Take in acount the scale (country, region, ...)
    """

    ax=plotseries(keyseries(nom,chiffre,evo),average)

    if chiffre in ["cas","nombre_de_cas","cas_confirmes"] and not evo :

        ax.set(title= "Prevalence of Covid-19 in "+nom,ylabel="case")

    elif chiffre in ["cas","nombre_de_cas","cas_confirmes"] and evo:

        ax.set(title= "Daily cases of Covid-19 in "+nom,ylabel="case")

    elif chiffre in ["hospitalisation","hôpital","hospitalises"] and evo:

        ax.set(title= "Daily extra patients of Covid-19\
             at the hospital in "+nom,ylabel="people hospitalized")

    elif chiffre in ["hospitalisation","hôpital","hospitalises"] and not evo:

        ax.set(title= "Number of patients of Covid-19\
         at the hospital in "+nom,ylabel="people hospitalized")

    elif chiffre in["deces_ehpad"] and not evo:

        ax.set(title= "Number of death of Covid-19 \
            in EHPADs in "+nom,ylabel="death")

    elif chiffre in["deces_ehpad"] and  evo:

        ax.set(title= "Number of death of Covid-19 in\
             EHPADs in "+nom,ylabel="death")

    elif chiffre in["deces","morts"] and  not evo:

        ax.set(title= "Number of deaths of Covid-19 \
             in "+nom,ylabel="death")

    elif chiffre in["deces","morts"] and   evo:

        ax.set(title= "New deaths of Covid-19\
              in "+nom,ylabel="death")

    elif chiffre in["reanimation"] and   evo:

        ax.set(title= "Daily extra patients in\
             intensive care because of Covid-19  in \
                 "+nom,ylabel="patients")

    elif chiffre in ["reanimation"] and not  evo:
    
        ax.set(title="Number of patients in intensive\
         care because of Covid-19 in"+nom,ylabel="patients")

    elif chiffre in ["cas_confirmes_ehpad"] and evo:
     
        ax.set(title="Daily cases of Covid-19 in\
         EHPADs"+nom,ylabel="cases")

    elif chiffre in ["cas_confirmes_ehpad"] and  not evo:

        ax.set(title="Prevalence of Covid-19 in\
             EHPADs"+nom,ylabel="cases")

    elif chiffre in ["gueris"] and  not evo:

        ax.set(title="Number of people cured from \
            Covid-19 "+nom,ylabel="people")

    elif chiffre in ["gueris"] and   evo:

        ax.set(title="Daily number of people \
            cured from Covid-19 "+nom,ylabel="people")
    plt.show()

#%%
keyplot("Hérault","cas",evo=False)

#keyseries("France","hôpital",evo=False)
#keyseries('Île-de-France','cas')
#keyplot('Île-de-France','cas')



# %%
keyseries("France","cas")
# %%

# %%
