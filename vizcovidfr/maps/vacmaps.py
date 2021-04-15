# ---------- requirements ----------
#%%
import os
import pandas as pd
from download import download
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

url = "https://public.opendatasoft.com/explore/dataset/covid-19-france-vaccinations-age-sexe-dep/export/?disjunctive.variable_label&sort=date&refine.date=2021&refine.variable=Par+tranche+d%E2%80%99%C3%A2ge"
path_target = "C:/Users/quenf/vizcovidfr/vizcovidfr/data/covid-19-france-vaccinations-age-dep.csv"


#%%

def vacmap(granularity, age_range):
    '''


    '''
    df_Vac = pd.read_csv(path_target, ";")
    df_Vac.sort_values(by=['Date', 'Valeur de la variable'], inplace=True)
    reg_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "regions.geojson")
    dep_path = os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    "geodata", "departements.geojson")
    rgn = gpd.read_file(reg_path)
    dpt = gpd.read_file(dep_path)
    
    df_Vac = df_Vac.groupby(['Valeur de la variable'])
    till_24 = df_Vac.get_group(24).reset_index(drop = True)
    till_29 = df_Vac.get_group(29).reset_index(drop = True)
    till_39 = df_Vac.get_group(39).reset_index(drop = True)
    till_49 = df_Vac.get_group(49).reset_index(drop = True)
    till_59 = df_Vac.get_group(59).reset_index(drop = True)
    till_64 = df_Vac.get_group(64).reset_index(drop = True)
    till_69 = df_Vac.get_group(69).reset_index(drop = True)
    till_74 = df_Vac.get_group(74).reset_index(drop = True)
    till_79 = df_Vac.get_group(79).reset_index(drop = True)
    sup_80 = df_Vac.get_group(80).reset_index(drop = True)
    all_ages = df_Vac.get_group(0).reset_index(drop = True) 
    # choose dataframe according to age_range argument
    if (age_range == '18-24'):
        df = till_24.copy()
        age = '18-24'
    elif (age_range == '25-29'):
        df = till_29.copy()
        age = '25-29'
    elif (age_range == '30-39'):
        df = till_39.copy()
        age = '30-39'
    elif (age_range == '40-49'):
        df = till_49.copy()
        age = '40-49'
    elif (age_range == '50-59'):
        df = till_59.copy()
        age = '50-59'
    elif (age_range == '60-24'):
        df = till_64.copy()
        age = '60-64'
    elif (age_range == '65-69'):
        df = till_69.copy()
        age = '65-69'
    elif (age_range == '70-74'):
        df = till_74.copy()
        age = '70-74'
    elif (age_range == '75-79'):
        df = till_79.copy()
        age = '65-79'
    elif (age_range == '80 and +'):
        df = sup_80.copy()
        age = '80 and +'
    elif (age_range == 'all ages'):
        df = all_ages.copy()
        age = 'all ages'
    # choose dataframe according to granularity argument
    if (granularity == 'departement'):
        df2 = dpt.copy()
        gra = 'department'
        df['code'] = df['Code Officiel Département']
        df3 = df.groupby(['Date', 'code'])['Nombre cumulé de doses n°1'].agg('sum').reset_index()
        df3 = df3.groupby(['code']).agg('max')#pick the latest cumule per granularity
        df3['code'] = df3.index
        df3.reset_index(drop=True, inplace=True)
        df3.drop([76, 97], 0, inplace=True) #non-existent departments
        df3.drop([98, 99, 100, 101, 102, 103, 104], 0, inplace=True) 
        #no localisation data for these departments
    else:
        df2 = rgn.copy()
        gra = 'region'
        df['code'] = df['Code Officiel Région']
        df3 = df.groupby(['Date', 'code'])['Nombre cumulé de doses n°1'].agg('sum').reset_index()
        df3 = df3.groupby(['code']).agg('max')#pick the latest cumule per granularity
        df3['code'] = df3.index
        df3.reset_index(drop=True, inplace=True)
        df3['code'] = df3['code'].astype(int)
        df3['code'] = df3['code'].astype(str)
        df3['code'][0] = '01'
        df3['code'][1] = '02'
        df3['code'][2] = '03'
        df3['code'][3] = '04'
        df3['code'][4] = '06'
        df3.drop([18, 19], 0, inplace=True) 
        #977 and 978 are departments and not regions
    # grab department centroids (lat and lon)
    df_points = df2.copy()
    df_points['geometry'] = df_points['geometry'].centroid
    # merge dataframes
    df_merged = pd.merge(df3, df_points, on='code')
    df_merged['lon'] = df_merged.geometry.apply(lambda p: p.x)
    df_merged['lat'] = df_merged.geometry.apply(lambda p: p.y)
    # ---------- make map! ----------
    # initialize view (centered on Paris!)
    view = pdk.ViewState(latitude = 46.232192999999995,
                         longitude = 2.209666999999996,
                         pitch = 50,
                         zoom = 6)
    covid_amount_layer = pdk.Layer('ColumnLayer',
                                   data = df_merged,
                                   get_position = ['lon', 'lat'],
                                   get_elevation = 'Nombre cumulé de doses n°1',
                                   elevation_scale = 100,
                                   radius = 7000,
                                   get_fill_color = [255, 165, 0, 80],
                                   pickable = True,
                                   auto_highlight = True)
    #save the map into a html file
    r = pdk.Deck(layers=[covid_amount_layer], initial_view_state=view)
    r.to_html('vacmaps.html')
