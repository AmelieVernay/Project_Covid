# ---------- requirements ----------
import pandas as pd

import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import date, datetime
import numpy as np
import folium
import os

import pydeck as pdk
import ipywidgets
from palettable.cartocolors.sequential import BrwnYl_3
import json

# local reqs
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_chiffres_cles
# add python option to avoid "false positive" warning:
pd.options.mode.chained_assignment = None  # default='warn'


# ---------- format some default arguments ----------

# get user's path to Desktop
A = os.path.expanduser("~")
B = "Desktop"
path_to_Desktop = os.path.join(A, B)

# format today's date
dt_today = date.today()
today = dt_today.strftime('%Y-%m-%d')


# ---------- define viz2Dmap ----------
def viz2Dmap(granularity='departement', date=today,
             criterion='hospitalises', color_pal='YlGnBu',
             file_path=path_to_Desktop, file_name='Covid2Dmap'):
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
        Should be of the form 'YYYY-MM-DD', and from 2020-01-24 to today,
        defaults to today.
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
        MAC-OS, or Windows path, defaults to user's Desktop.
        **Warning:** only works if the user's OS default language is english.
        Otherwise, path is not optional.
    :type file_path: str
    :param file_name: the name under which to save the file,
        defaults to 'Covid2Dmap'
    :type file_name: str

    Returns
    -------
    :return: An interactive choropleth map saved on a html file openable on
        your favorite web browser
    :rtype: '.html' file

    Examples
    --------
    **easy example**
    >>>viz2Dmap()

    **example using Linux path**

    >>> import os
    >>> path_to_desktop = os.path.expanduser("~/Desktop")
    >>> viz2Dmap(granularity='region', date='2020-12-25', criterion='deces',
    ...          color_pal='Greys', file_path=path_to_desktop,
    ...          file_name='creepymap')

    **example using Windows path**

    >>> import os
    >>> W_path = 'c:\\Users\\username\\Documents'
    >>> viz2Dmap(granularity='department', date='2021-01-17',
    ...          criterion='reanimation', color_pal='Greys',
    ...          file_path=W_path, file_name='funkymap')

    Notes
    -----
    **Manipulation tips:**

    - pass mouse on map to get local informations
    - use 'clic + mouse move' to move map
    '''
    # ---------- file imports ----------
    # load geojson file containing geographic informations
    reg_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "regions.geojson")
    dep_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "departements.geojson")
    regions = gpd.read_file(reg_path)
    departments = gpd.read_file(dep_path)
    # load covid data
    df_covid = load_datasets.Load_chiffres_cles().save_as_df()
    # ---------- preprocesses ----------
    # use preprocess to clean df_covid
    df_covid = preprocess_chiffres_cles.drop_some_columns(df_covid)
    df_covid = preprocess_chiffres_cles.reg_depts(df_covid)
    df_covid = preprocess_chiffres_cles.reg_depts_code_format(df_covid)
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
            fill_color=color_pal,
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
# NOTE: it worked without importing df_covid...


# ---------- define viz3Dmap ----------
def viz3Dmap(granularity='departement', criterion='hospitalises',
             file_path=path_to_Desktop, file_name='3Dmap_Covid',
             color=[255, 165, 0, 80]):
    '''
    Make a 3D map out of France Covid-19 data.
    Layers elevation represent the amount of death for the given place at a
    given day, which can be view by passing the mouse on it.

    Parameters
    ----------
    :param granularity: the granularity we want the map to be based on.
        Should be either 'region' or 'departement'. On the latter case,
        columns layers will be raised from the centroid of each department,
        while on the former, these will be raides from each region's centroid.
        Defaults to 'department'.
    :type granularity: string
    :param criterion: the Covid-19 indicator we want to see on the map.
        Should be either 'hospitalises', 'reanimation', or 'deces':

        - 'hospitalises': will display to number of persons hospitalized
            on a given date due to Covid-19
        - 'reanimation': will display to number of persons in resuscitation
            on a given date due to Covid-19
        - 'deces': will display to cumulated number of death due to
            the Covid-19 in France from the beginning of the pandemic, up to
            a given date

        defaults to 'hospitalises'.
    :type criterion: str
    :param color: color for columns. Should be a list
        containing RGBA colors (red, green, blue, alpha).
        For example, see here https://rgbacolorpicker.com/,
        defaults to yellow (sort of)
    :type color: str
    :param file_path: the path on which to save the file, can be either Linux,
        MAC-OS, or Windows path, defaults to user's Desktop.
        **Warning:** only works if the user's OS default language is english.
        Otherwise, path is not optional.
    :type file_path: str
    :param file_name: the name under which to save the file,
        defaults to '3Dmap_Covid'
    :type file_name: str

    Returns
    -------
    :return: An interactive 3D map saved on a html file openable on
        your favorite web browser
    :rtype: '.html' file

    Examples
    --------
    **easy example**
    >>> viz3Dmap()

    **example using Linux path**
    >>> import os
    >>> path_to_desktop = os.path.expanduser("~/Desktop")
    >>> viz3Dmap(file_path=path_to_desktop, file_name='pinky_3D_map',
    ...          granularity='departement', criterion='reanimation',
    ...          color=[245, 92, 245, 80])

    **example using Windows path**
    >>> import os
    >>> W_path = 'c:\\Users\\username\\Documents'
    >>> viz3Dmap(file_path=W_path, color=[230, 37, 37, 80],
    ...          criterion='deces')

    Notes
    -----

    The bottom of the map corresponds to the beginning of the Covid-19
    pandemic in France, specifically here, data start on 2020-01-24. The top
    of the columns corresponds to now.

    **Manipulation tips:**

    - pass mouse on columns to see time evolution
    - use 'ctrl + mouse move' to change view angle
    - use 'clic + mouse move' to move map
    '''
    # ---------- file imports ----------
    # geo files
    reg_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "regions.geojson")
    dep_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "departements.geojson")
    reg = gpd.read_file(reg_path)
    dep = gpd.read_file(dep_path)
    # covid files
    df_covid = load_datasets.Load_chiffres_cles().save_as_df()
    # ---------- preprocesses ----------
    df_covid = preprocess_chiffres_cles.drop_some_columns(df_covid)
    df_covid = preprocess_chiffres_cles.reg_depts(df_covid)
    df_covid = preprocess_chiffres_cles.reg_depts_code_format(df_covid)
    # choose dataframe according to granularity argument
    if (granularity == 'departement'):
        df = dep.copy()
        gra = 'department'
    else:
        df = reg.copy()
        gra = 'region'
    # format crierion for markers purpose
    if (criterion == 'hospitalises'):
        tooltip = {
            "html": "<b>Place:</b> {nom} <br /><b>Date:</b> {date}\
            <br /><b>Number of hospitalization:</b> {hospitalises}"}
    elif (criterion == 'reanimation'):
        tooltip = {
            "html": "<b>Place:</b> {nom} <br /><b>Date:</b> {date}\
            <br /><b>Number of persons in resuscitation:</b> {reanimation}"}
    else:
        tooltip = {
            "html": "<b>Place:</b> {nom} <br /><b>Date:</b> {date}\
            <br /><b>Cumulated number of death:</b> {deces}"}
    # for covid data
    df_local = df_covid.loc[df_covid['granularite'] == granularity]
    # for geo data
    # grab department's centroids (lat and lon)
    df_points = df.copy()
    # set Europe Coordinate Reference System for geographic accuracy purpose
    df_points = df_points.set_crs(epsg=3035, allow_override=True)
    df_points['geometry'] = df_points['geometry'].centroid
    # merging on 'code'
    A = pd.merge(df_local, df_points, on='code')
    # separate latitude and longitude
    A['lon'] = A.geometry.apply(lambda p: p.x)
    A['lat'] = A.geometry.apply(lambda p: p.y)
    # ---------- make map! ----------
    # initialize view (centered on Paris!)
    view = pdk.ViewState(latitude=46.232192999999995,
                         longitude=2.209666999999996,
                         pitch=50,
                         zoom=5.5)
    # add pydeck layers
    covid_amount_layer = pdk.Layer('ColumnLayer',
                                   data=A,
                                   get_position=['lon', 'lat'],
                                   get_elevation=criterion,
                                   elevation_scale=100,
                                   radius=7000,
                                   get_fill_color=color,
                                   pickable=True,
                                   auto_highlight=True)
    # render map
    covid_amount_layer_map = pdk.Deck(layers=covid_amount_layer,
                                      initial_view_state=view,
                                      tooltip=tooltip)
    # save map
    suffix = '.html'
    save_path = os.path.join(file_path, file_name + suffix)
    covid_amount_layer_map.to_html(save_path)


# ---------- define transfer_map ----------
def transfer_map(file_path=path_to_Desktop, file_name='Covid_transfer_map',
                 color_d=[243, 31, 44, 80], color_a=[230, 190, 37, 80]):
    """
    Make interactive 3D-arc-map to visualize the transfer of Covid-19
    patient in France from regions to others.

    Parameters
    ----------
    :param file_path: the path on which to save the file, can be either Linux,
        MAC-OS, or Windows path, defaults to user's Desktop.
        **Warning:** only works if the user's OS default language is english.
        Otherwise, path is not optional.
    :type file_path: str
    :param file_name: the name under which to save the file,
        defaults to 'Covid_transfer_map'
    :type file_name: str
    :param color_d: color for departure point on arcs. Should be a list
        containing RGBA colors (red, green, blue, alpha).
        For example, see here https://rgbacolorpicker.com/,
        defaults to red (sort of)
    :type color_d: list
    :param color_a: color for arrival point on arcs. Should be a list
        containing RGBA colors (red, green, blue, alpha).
        For example, see here https://rgbacolorpicker.com/,
        defaults to yellow (sort of)
    :type color_a: list

    Returns
    -------
    :return: An interactive 3D-arc-map saved on a html file openable on
        your favorite web browser
    :rtype: '.html' file

    Examples
    --------
    **easy example**
    >>>transfer_map()

    **example using Linux path**
    >>> import os
    >>> path_to_desktop = os.path.expanduser("~/Desktop")
    >>> transfer_map(file_path=path_to_desktop, file_name='pinky_arc_map',
    ...          color_d=[255, 165, 0, 80], color_a=[128, 0, 128, 80])

    **example using Windows path**
    >>> import os
    >>> W_path = 'c:\\Users\\username\\Documents'
    >>> transfer_map(file_path=W_path, file_name='counter_intuitive_arc_map',
    ...          color_d=[61, 230, 37, 80], color_a=[230, 37, 37, 80])

    Notes
    -----
    **Manipulation tips:**

    - pass mouse on arc to see tooltip
    - use 'ctrl + mouse move' to change view angle
    - use 'clic + mouse move' to move map
    """
    # ---------- covid file ----------
    transfer = load_datasets.Load_transfer().save_as_df()
    # Keep trace of transfer order
    # because rows get mixed up when merging.
    # number transfer from first to last
    transfer_order = np.arange(0, len(transfer), 1)
    # add transfer_order column
    transfer['order'] = transfer_order
    # ---------- geo files ----------
    # only need regions here
    reg_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "regions.geojson")
    regions = gpd.read_file(reg_path)
    # grab region's centroids (lat and lon)
    region_points = regions.copy()
    # set Europe Coordinate Reference System for geographic accuracy purpose
    region_points = region_points.set_crs(epsg=3035, allow_override=True)
    region_points['geometry'] = region_points['geometry'].centroid
    # extract departure informations
    departure = transfer[['region_depart', 'order', 'debut_transfert']]
    departure['nom'] = departure['region_depart']
    # extract departure informations
    arrival = transfer[['region_arrivee',
                        'nombre_patients_transferes',
                        'order']]
    arrival['nom'] = arrival['region_arrivee']
    # get departure and arrival geographic coordinates
    D = pd.merge(departure, region_points, on="nom")
    A = pd.merge(arrival, region_points, on="nom")
    # extract latitude and longitude
    # for departure
    D['lon_d'] = D.geometry.apply(lambda p: p.x)
    D['lat_d'] = D.geometry.apply(lambda p: p.y)
    # for arrival
    A['lon_a'] = A.geometry.apply(lambda p: p.x)
    A['lat_a'] = A.geometry.apply(lambda p: p.y)
    # delete not-useful-anymore columns for clarity purpose
    del D['nom']
    del D['geometry']
    del A['nom']
    del A['geometry']
    # merge these new dataframes together
    # (on order so that we have our chronology back!)
    DA = pd.merge(A, D, on='order')
    # save for sparse matrix purpose ?
    # DA.to_csv('departure_arrival.csv')
    # ---------- map time! ----------
    # initialize view (centered on Paris!)
    view = pdk.ViewState(latitude=46.2322, longitude=2.20967, pitch=50, zoom=5)
    # make arc layers from departure to arrival points
    arc_layer = pdk.Layer('ArcLayer',
                          data=DA,
                          get_source_position=['lon_d', 'lat_d'],
                          get_target_position=['lon_a', 'lat_a'],
                          get_width=5,
                          get_tilt=15,
                          get_source_color=color_d,
                          get_target_color=color_a,
                          # interactivity
                          pickable=True,
                          auto_highlight=True)
    # add tooltip
    tooltip = {
            "html": "<b>Date:\
            </b> {debut_transfert} <br />\
            <b>Number of transfered patient:\
            </b> {nombre_patients_transferes} <br />\
            <b>Departure region:</b> {region_depart} <br />\
            <b>Arrival region:</b> {region_arrivee}\
            "}
    # add view and layer to map
    arc_layer_map = pdk.Deck(layers=arc_layer,
                             initial_view_state=view,
                             tooltip=tooltip)
    # save map
    suffix = '.html'
    save_path = os.path.join(file_path, file_name + suffix)
    arc_layer_map.to_html(save_path)


# TODO:
# remove # save for sparse matrix purpose ? if not needed
