# ---------- requirements ----------
import time
import pandas as pd
from download import download
import datetime
import plotly.express as px

# local reqs
from vizcovidfr.loads import load_datasets

# add python option to avoid "false positive" warning:
pd.options.mode.chained_assignment = None  # default='warn'

# line chart representing the french vaccine storage per vaccine type


def vactypedoses(vaccine_type='All vaccines', color_pal='darkblue',
                 color_pal2='crimson', color_pal3='darkgreen',
                 font_size=16, font_family="Franklin Gothic Medium",
                 font_color='white', bgcolor='darkslategrey',
                 template='plotly_dark'):
    '''
    Make animated line chart of France vaccine data.

    Parameters
    ----------
    :param vaccine_type: the vaccine type we want to display.
        Either 'Pfizer', 'Moderna', 'AstraZeneca' or 'All vaccines'.
        In this latter case, the three vaccine types are represented.
        It is possible to hover one's mouse over the curves to get thorough
        information.
    :type vaccine_type: str, optional, default='All vaccines'
    :param color_pal: the color of the chosen vaccine type curve.
        If 'All vaccines' vaccine_type is chosen, sets the color of the
        'Pfizer' curve.

        For reference, see http://www.python-simple.com/img/img45.png.
    :type color_pal: str, optional, default='darkblue'
    :param color_pal2: Only if 'All vaccines' vaccine_type is chosen.
        Set the color of 'Moderna' curve.

        For reference, see http://www.python-simple.com/img/img45.png.
    :type color_pal2: str, optional, default='crimson'
    :param color_pal3: Only if 'All vaccines' vaccine_type is chosen.
        Set the color of 'AstraZeneca' curve.

        For reference, see http://www.python-simple.com/img/img45.png.
    :type color_pal3: str, optional, default='darkgreen'
        :param font_size: the size of characters in hover labels
    :type font_size: int, optional, default=16
    :param font_family: the font family of the characters in hover labels.

        For reference, see
        http://jonathansoma.com/site/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/
    :type font_family: str, optional, default='Franklin Gothic Medium'
    :param font_color: the color of characters in hover labels,
        For reference, see http://www.python-simple.com/img/img45.png.
    :type font_color: str, optional, default='white'
    :param bgcolor: the background color of all hover labels on graph.
        For reference, see http://www.python-simple.com/img/img45.png.
    :type bgcolor: str, optional, default='darkslategrey'
    :param template: the plotly theme

        For reference, see https://plotly.com/python/templates/.
    :type template: str, optional, default='plotly_dark'

    Returns
    -------
    :return: animated line chart representing the actual
        dose number of the chosen vaccine type (in storage).
    :rtype: plotly.graph_objects.Figure
    '''
    start = time.time()
    df_Vac_type = load_datasets.Load_Vaccine_storage().save_as_df()
    df_Vac_type2 = df_Vac_type.groupby(['type_de_vaccin'])
    pfizer = df_Vac_type2.get_group('Pfizer').reset_index(drop=True)
    mdn = df_Vac_type2.get_group('Moderna').reset_index(drop=True)
    astra = df_Vac_type2.get_group('AstraZeneca').reset_index(drop=True)

    # choose dataframe according to vaccine_type argument
    if (vaccine_type == 'Pfizer'):
        df = pfizer.copy()
        vac_type = 'Pfizer'
        fig = px.line(df,
                      x='date',
                      y='nb_doses',
                      color='type_de_vaccin',
                      color_discrete_map={'Pfizer': color_pal},
                      title='Pfizer vaccine storage in France')
    elif (vaccine_type == 'Moderna'):
        df = mdn.copy()
        vac_type = 'Moderna'
        fig = px.line(df,
                      x='date',
                      y='nb_doses',
                      color='type_de_vaccin',
                      color_discrete_map={'Moderna': color_pal},
                      title='Moderna vaccine storage in France')
    elif (vaccine_type == 'AstraZeneca'):
        df = astra.copy()
        vac_type == 'AstraZeneca'
        fig = px.line(df,
                      x='date',
                      y='nb_doses',
                      color='type_de_vaccin',
                      color_discrete_map={'AstraZeneca': color_pal},
                      title='AstraZeneca vaccine storage in France')
    elif (vaccine_type == 'All vaccines'):
        df = df_Vac_type.copy()
        vac_type = 'ALL'
        fig = px.line(df,
                      x='date',
                      y='nb_doses',
                      color='type_de_vaccin',
                      color_discrete_map={'Pfizer': color_pal,
                                          'Moderna': color_pal2,
                                          'AstraZeneca': color_pal3},
                      title='Vaccine storage in France',
                      template=template)
    fig.update_traces(mode="markers + lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        hoverlabel=dict(
            bgcolor='lightslategrey',
            font_color='white',
            font_size=16,
            font_family="Franklin Gothic Medium"
            )
        )
    # displaying line chart according to vaccine_type argument
    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))
    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))
    fig.show()

# how to display the year of each date?


# Test:
# vactypedoses()


# line chart with total number of vaccine doses in storage
def vacdoses(unit='doses', font_size=16,
             font_family="Franklin Gothic Medium",
             font_color='white', bgcolor='darkslategrey',
             template='plotly_dark'):
    '''
    Make an interactive line chart of France vaccine data.

    Parameters
    ----------
    :param unit: the type of dose units we want to display.
        Either 'doses' or 'cdu' (shorts for 'common dispensing units'),

        - 'doses':
            display the evolution of total vaccine doses in storage,
            from January 2021 until now. (checkouts are not made everyday).
        - 'cdu':
            display the evolution of total vaccine bottles in storage,
            from January 2021 until now. (checkouts are not made everyday).

        For 'Pfizer' vaccine, the cdu conversion rate per dose
        is multiplied by 6.
        For Moderna and AstraZeneca vaccines, the cdu conversion rate per dose
        is multiplied by 10.
    :type unit: str, optional, default = 'doses'
    :param font_size: the size of characters in hover labels.
    :type font_size: int, optional, default = 16
    :param font_family: the font family of the characters in hover labels.
        For reference, see
        http://jonathansoma.com/site/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/.
    :type font_family: str, optional, default = 'Franklin Gothic Medium'
    :param font_color: the color of characters in hover labels,.
        For reference, see http://www.python-simple.com/img/img45.png.
    :type font_color: str, optional, default = 'white'
    :param bgcolor: the background color of all hover labels on graph.

        For reference, see http://www.python-simple.com/img/img45.png.
    :type bgcolor: str, optional, default = 'darkslategrey'
    :param template: the theme of plotly.

        For reference, see https://plotly.com/python/templates/.
    :type template: str, optional, default = 'plotly_dark'

    Returns
    -------
    :return: An interactive line chart representing the actual
        amount in storage of vaccine doses, according to the chosen unit.
    :rtype: plotly.graph_objects.Figure
    '''
    start = time.time()
    df_Vac_type = load_datasets.Load_Vaccine_storage().save_as_df()
    df = df_Vac_type.groupby(['date'])['nb_doses',
                                       'nb_ucd'].agg('sum').reset_index()
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
    # display line chart according to unit argument
    fig = px.line(
                df,
                x='date',
                y=nbr,
                title=f"Evolution of vaccine {a} number in storage in France",
                template=template)
    fig.update_traces(mode="markers + lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=bgcolor,
            font_color=font_color,
            font_size=font_size,
            font_family=font_family
            ))
    end = time.time()
    print("Time to execute: {0:.5f} s.".format(end - start))
    fig.show()


# Test:
# vacdoses()
