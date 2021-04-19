# ---------- requirements ----------
import pandas as pd
from download import download
pd.options.display.max_rows = 25
import datetime
import plotly.express as px

from vizcovidfr.loads import load_datasets


#line chart representing the french vaccine storage per vaccine type 
df_Vac_type = load_datasets.Load_Vaccine_storage().save_as_df()


def vactypedoses(vaccine_type = 'All vaccines', color_pal = 'darkblue', 
                color_pal2 = 'crimson', 
                color_pal3 = 'darkgreen', font_size = 16, 
                font_family = "Franklin Gothic Medium",
                font_color = 'white', bgcolor = 'darkslategrey', 
                template = 'plotly_dark'):
    '''
    Make an animated line chart of France vaccine data.

    Parameters
    ----------
    :param vaccine_type: the vaccine type we want to display.
        Either 'Pfizer', 'Moderna', 'AstraZeneca' or 'All vaccines'.
        In this latter case, the three vaccine types are represented.
        It is possible to hover one's mouse over the curves to get thorough information. 
    :type vaccine_type: str
    :param color_pal: Sets the color of the chosen vaccine type curve.
        If 'All vaccines' vaccine_type is chosen, sets the color of the 'Pfizer' curve.
        For reference, see http://www.python-simple.com/img/img45.png.
        Defaults to 'darkblue'.
    :type color_pal: str
    :param color_pal2: Only if 'All vaccines' vaccine_type is chosen.
        Sets the color of 'Moderna' curve.
        For reference, see http://www.python-simple.com/img/img45.png.
        Defaults to 'crimson'.
    :type color_pal2: str
    :param color_pal3: Only if 'All vaccines' vaccine_type is chosen.
        Sets the color of 'AstraZeneca' curve.
        For reference, see http://www.python-simple.com/img/img45.png.
        Defaults to 'darkgreen'.
    :type color_pal3: str
        :param font_size: Sets the size of characters in hover labels, defaults to 16.
    :type font_size: int
    :param font_family: Sets the font family of the characters in hover labels. 
        For reference, see 
        http://jonathansoma.com/site/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/,
        defaults to 'Franklin Gothic Medium'.
    :type font_family: str
    :param font_color: Sets the color of characters in hover labels,
        For reference, see http://www.python-simple.com/img/img45.png, 
        defaults to 'white'.
    :type font_color: str
    :param bgcolor: Sets the background color of all hover labels on graph.
        For reference, see http://www.python-simple.com/img/img45.png, 
        defaults to 'darkslategrey'.
    :type bgcolor: str
    :param template: Sets the theme of plotly.
        For reference, see https://plotly.com/python/templates/,
        defaults to 'plotly_dark'. 
    :type template: str

    Returns
    -------
    :return: an animated line chart representing the actual 
    dose number of the chosen vaccine type (in storage).
    :rtype: plotly.graph_objects.Figure
    '''
    df_Vac_type2 = df_Vac_type.groupby(['type_de_vaccin'])
    pfizer = df_Vac_type2.get_group('Pfizer').reset_index(drop = True)
    mdn = df_Vac_type2.get_group('Moderna').reset_index(drop = True)
    astra = df_Vac_type2.get_group('AstraZeneca').reset_index(drop = True)
    
    # choose dataframe according to vaccine_type argument 
    if (vaccine_type == 'Pfizer'):
        df = pfizer.copy()
        vac_type = 'Pfizer'
        fig = px.line(df, x = 'date', y = 'nb_doses', color = 'type_de_vaccin', color_discrete_map = {'Pfizer': color_pal}, title = 'Pfizer vaccine storage in France')
    elif (vaccine_type == 'Moderna'):
        df = mdn.copy()
        vac_type = 'Moderna'
        fig = px.line(df, x = 'date', y = 'nb_doses', color = 'type_de_vaccin', color_discrete_map = {'Moderna': color_pal}, title = 'Moderna vaccine storage in France')
    elif (vaccine_type == 'AstraZeneca'):
        df = astra.copy()
        vac_type == 'AstraZeneca'
        fig = px.line(df, x = 'date', y = 'nb_doses', color = 'type_de_vaccin', color_discrete_map = {'AstraZeneca': color_pal}, title = 'AstraZeneca vaccine storage in France')
    elif (vaccine_type == 'All vaccines'):
        df = df_Vac_type.copy()
        vac_type = 'ALL'
        fig = px.line(df, x = 'date', y = 'nb_doses', color = 'type_de_vaccin', color_discrete_map={'Pfizer': color_pal,'Moderna': color_pal2,'AstraZeneca': color_pal3}, title = 'Vaccine storage in France', template = template)
    fig.update_traces(mode= "markers+lines", hovertemplate=None)
    fig.update_layout(hovermode = "x unified")
    fig.update_layout(
    hoverlabel = dict(
        bgcolor = 'lightslategrey',
        font_color = 'white',
        font_size = 16,
        font_family = "Franklin Gothic Medium"
    ))
    # displaying line chart according to vaccine_type argument
    fig.show()

#how to display the year of each date?


#Test
#vactypedoses()

#line chart with total number of vaccine doses in storage
def vacdoses(unit = 'doses', font_size = 16, 
            font_family = "Franklin Gothic Medium",
            font_color = 'white', bgcolor = 'darkslategrey',
            template = 'plotly_dark'):
    '''
    Make an interactive line chart of France vaccine data.

    Parameters
    ----------
    :param unit: the type of dose units we want to display.
        Either 'doses' or 'cdu' (shorts for 'common dispensing units'), 
        
        - 'doses': will display the evolution of total vaccine doses in storage,
                from January 2021 until now. (checkouts are not made everyday).
        - 'cdu': will display the evolution of total vaccine bottles in storage, 
                from January 2021 until now. (checkouts are not made everyday).

        For 'Pfizer' vaccine, the cdu conversion rate per dose is multiplied by 6.
        For Moderna and AstraZeneca vaccines, the cdu conversion rate per dose is multiplied by 10.
        Defaults to 'doses'.
    :type unit: str
    :param font_size: Sets the size of characters in hover labels, defaults to 16.
    :type font_size: int
    :param font_family: Sets the font family of the characters in hover labels. 
        For reference, see 
        http://jonathansoma.com/site/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/,
        defaults to 'Franklin Gothic Medium'.
    :type font_family: str
    :param font_color: Sets the color of characters in hover labels,.
        For reference, see http://www.python-simple.com/img/img45.png, 
        defaults to 'white'.
    :type font_color: str
    :param bgcolor: Sets the background color of all hover labels on graph.
        For reference, see http://www.python-simple.com/img/img45.png, 
        defaults to 'darkslategrey'.
    :type bgcolor: str
    :param template: Sets the theme of plotly.
        For reference, see https://plotly.com/python/templates/,
        defaults to 'plotly_dark'. 
    :type template: str

    Returns
    -------
    :return: An interactive line chart representing the actual
    amount in storage of vaccine doses, according to the chosen 
    unit.
    :rtype: plotly.graph_objects.Figure
    '''
    df = df_Vac_type.groupby(['date'])['nb_doses', 'nb_ucd'].agg('sum').reset_index()
    doses = df.groupby(['date'])['nb_doses'].size().reset_index()
    ucd = df.groupby(['date'])['nb_ucd'].size().reset_index()
    doses['nb_doses'] = df['nb_doses']
    ucd['nb_ucd'] = df['nb_ucd']
    if (unit == 'doses'):
        df = doses.copy()
        nbr = 'nb_doses'
        a = 'dose'
    else:
        df = ucd.copy()
        nbr = 'nb_ucd'
        a = 'cdu'
    #displaying a line chart according to unit argument
    fig = px.line(df, x = 'date', y = nbr, title = "Evolution of vaccine %s number in storage (in France)" % a, template = template)
    fig.update_traces(mode= "markers+lines", hovertemplate=None)
    fig.update_layout(hovermode = "x unified")
    fig.update_layout(
    hoverlabel = dict(
        bgcolor = bgcolor,
        font_color = font_color,
        font_size = font_size,
        font_family = font_family
    ))
    fig.show()

#Test
#vacdoses()




# %%
