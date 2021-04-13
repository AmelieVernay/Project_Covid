# ---------- requirements ----------

import os

# map reqs
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

import pydeck as pdk
from vega_datasets import data as vds
import ipywidgets
from palettable.cartocolors.sequential import BrwnYl_3
import json

# local reqs
from vizcovidfr.loads import load_datasets
from vizcovidfr.preprocesses import preprocess_chiffres_cles


def make_3D_map(granularity):
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
    # for covid data
    df_local = df_covid.loc[df_covid['granularite'] == granularity]
    # for geo data
    # grab department's centroids (lat and lon)
    df_points = df.copy()
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
                         zoom=6)
    # add pydeck layers
    covid_amount_layer = pdk.Layer('ColumnLayer',
                                   data=A,
                                   get_position=['lon', 'lat'],
                                   get_elevation='deces',
                                   elevation_scale=100,
                                   radius=7000,
                                   get_fill_color=[255, 165, 0, 80],
                                   pickable=True,
                                   auto_highlight=True)
    # render map
    covid_amount_layer_map = pdk.Deck(layers=covid_amount_layer,
                                      initial_view_state=view)
    # save map
    covid_amount_layer_map.to_html('3Dmap_covid.html')


# To try:
# make_3D_map('region')

# TODO:
# ADD DOCSTRING !!
# add possibility to change 'deces'
# change save path
# try to make polygon layers instead of ColumnLayer
# change markers aspect
# change color ?
