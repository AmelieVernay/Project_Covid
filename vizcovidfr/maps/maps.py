# ---------- requirements ----------
import pandas as pd

import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import date, datetime
import folium
import os

from python_files.loads import tryit
from python_files.preprocess import preprocess_data
# add python option to avoid "false positive" warning:
pd.options.mode.chained_assignment = None  # default='warn'


# ---------- define viz2Dmap ----------
def viz2Dmap(granularity, date, criterion, color_pal, file_path, file_name):
    '''
    Make interactive choropleth map to visualize different aspects of the
    Covid-19 pandemic in France. The map is saved on an html file at a given
    path on a given name, see function parameters for details.

    Parameters
    ----------

    :param granularity: the granularity we want the map to be based on.
        Should be either 'region' or 'departement', defaults to 'departement'.
    :type granularity: str
    :param date: the date on which we want to get Covid-19 informations.
        Should be of the form 'YYYY-MM-DD', defaults to today.
    :type date: str
    :param criterion: the Covid-19 indicator we want to see on the map.
        Should be either 'hospitalises', 'reanimation', or 'deces':

        - 'hospitalises': will display to number of persons hospitalized
            on the given date due to Covid-19
        - 'reanimation': will display to number of persons in resuscitation
            on the given date due to Covid-19
        - 'deces': will display to cumulated number of death due to
            the Covid-19 in France from the beginning of the pandemic, up to
            the given date

        defaults to 'hospitalises'.
    :type criterion: str
    :param color_pal: the color palette we want for the map.
        For reference,
        see https://colorbrewer2.org/#type=sequential&scheme=YlGnBu&n=3,
        defaults to 'YlGnBu' (for color-blind people purpose)
    :type color_pal: str
    :param file_path: the path on which to save the file, can be either Linux,
        MAC-OS, or Windows path, defaults to user's Desktop
    :type file_path: str
    :param file_name: the name under which to save the file,
        defaults to 'Covid2Dmap'
    :type file_name: str

    Returns
    -------

    :return: An interactive choropleth map save on a html file openable on
        your favorite web browser
    :rtype: '.html' file

    Examples
    --------

    **example using Linux path**

    >>> import os
    >>> path_to_desktop = os.path.expanduser("~/Desktop")
    >>> viz2Dmap(granularity='region', date='2020-12-25', criterion='deces',
    ...          color_pal='Greys', file_path=path_to_desktop,
    ...          file_name='creepymap')

    **example using Windows path**

    >>> import os
    >>> W_path = 'c:\Users\username\Documents'
    >>> viz2Dmap(granularity='department', date='2021-01-17',
    ...          criterion='reanimation', color_pal='Greys',
    ...          file_path=W_path, file_name='funkymap')

    '''
    # ---------- file imports ----------
    # load geojson file containing geographic informations
    departments = gpd.read_file('departements.geojson')
    regions = gpd.read_file('regions.geojson')
    # load covid data
    df_covid = tryit.Load_covid_data().save_as_df()
    # ---------- preprocesses ----------
    # use preprocess to clean df_covid
    df_covid = preprocess_data.preprocess_chiffres_clefs(df_covid)
    df_covid = preprocess_data.reg_depts(df_covid)
    df_covid = preprocess_data.reg_depts_code_format(df_covid)
    # keep only data corresponding to the given granularity
    df_local = df_covid.loc[df_covid['granularite'] == granularity]
    # choose the dataframe containing geographic
    # informations according to the granularity
    # (plus english precision)
    if (granularity == 'departement'):
        df = departments.copy()
        gra = 'department'
    else:
        df = regions.copy()
        gra = 'region'
    # merge on the 'code' column
    df_merged = pd.merge(df_local, df, on="code")
    # keep only data corresponding to the given date
    at_date = df_merged.loc[df_merged['date'] == date]
    # convert to GeoPandas dataframe
    gpd_at_date = gpd.GeoDataFrame(at_date)
    # -------- format legend ----------
    # format date for legend purpose
    given_date = datetime.strptime(date, '%Y-%m-%d')
    given_date = given_date.strftime("%A %d. %B %Y")
    # format crierion for legend purpose
    if (criterion == 'hospitalises'):
        formulated_criterion = 'hospitalization'
    elif (criterion == 'reanimation'):
        formulated_criterion = 'resuscitation'
    else:
        formulated_criterion = 'death'
    # change legend and title according to criterion
    if (criterion == 'deces'):
        legend = f'Cumulated number of {formulated_criterion} per {gra}'
        title = f'Cumulated number of {formulated_criterion} per {gra} in\
                France from the beginning of the pandemic up to {given_date}'
    else:
        legend = f'Number of {formulated_criterion} per {gra}'
        title = f'Number of {formulated_criterion} per {gra}\
                in France on {given_date}'
    # ---------- make map! ----------
    # initialize view (centered on Paris!)
    map = folium.Map(location=[46.2322, 2.20967], zoom_start=6, tiles=None)
    folium.TileLayer('CartoDB positron',
                     name="Light Map",
                     control=False).add_to(map)
    # add choropleth
    map.choropleth(
            geo_data=gpd_at_date,
            name='Choropleth',
            data=gpd_at_date,
            columns=['code', criterion],
            key_on="feature.properties.code",
            fill_color=color_palette,
            fill_opacity=1,
            line_opacity=0.2,
            legend_name=legend,
            smooth_factor=0
    )
    # Pep8 doesn't seem to like lambda expressions...
    # but I do, so I let these like that
    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}
    # make interactivity!
    geo_interact = folium.features.GeoJson(
                            gpd_at_date,
                            style_function=style_function,
                            control=False,
                            highlight_function=highlight_function,
                            tooltip=folium.features.GeoJsonTooltip(
                                fields=['nom', 'date', criterion],
                                style=("background-color: white;\
                                color: #333333; font-family: arial;\
                                font-size: 12px; padding: 10px;")
                                ))
    # add interactivity to the initial map
    map.add_child(geo_interact)
    # keep interactive layer on top of the map
    map.keep_in_front(geo_interact)
    folium.LayerControl().add_to(map)
    # add title
    title_html = '''
                 <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                 '''.format(title)
    map.get_root().html.add_child(folium.Element(title_html))
    # save map
    suffix = '.html'
    save_path = os.path.join(file_path, file_name + suffix)
    map.save(save_path)


# TODO:
# set default parameters
# td = date.today()
# add interval for date ("should be from ... to ...")
# NOTE: it worked without importing df_covid...
