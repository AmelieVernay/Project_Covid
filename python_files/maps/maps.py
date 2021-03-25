# ---------- requirements ----------
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

# ---------- NOTE ----------
# Maybe we should add this in the function
# so that the data always stay up to date.
# Or better: call in the function another
# one in an other file that expressly loads
# data every time it is called.
# The code should look something like this:
# url = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
# path_target = "./chiffres-cles.csv"
# download(url, path_target, replace=True)
# df_covid = pd.read_csv("chiffres-cles.csv")


# ---------- main function ----------
def vizmap_death(granularity):
    '''
    Input:
        granularity: string corresponding to the scale
                     we want the map to have
    Output:
        a map representing the actual number of death per
        region or department (according to the granularity chosen)
    '''
    # load the dataframes
    dpt = gpd.read_file('departements-version-simplifiee.geojson')
    rgn = gpd.read_file('regions-version-simplifiee.geojson')
    df_covid = pd.read_csv("chiffres-cles.csv")
    # choose the dataframe containing geographic
    # informations according to the granularity
    # (plus english precision)
    if (granularity == 'departement'):
        df = dpt.copy()
        gra = 'department'
    else:
        df = rgn.copy()
        gra = 'region'
    # only data concerning the chosen granularity
    df_local = df_covid.loc[df_covid['granularite'] == granularity]
    df_local = df_local.dropna(subset=['deces'])
    # keep only relevent informations
    df1 = df_local[['maille_code', 'maille_nom', 'deces']]
    df1 = df1.groupby(['maille_nom']).max()
    # format the 'code' strings
    for i in range(len(df1['maille_code'])):
        df1['maille_code'].iloc[i] = df1['maille_code'].iloc[i][4:]
    df1['code'] = df1['maille_code']
    del df1['maille_code']
    # set common index
    df1.set_index('code', inplace=True)
    df.set_index('code', inplace=True)
    # define new joined GeoDataFrame
    together = df1.join(df)
    together = gpd.GeoDataFrame(together)
    # ----- Plotting part -----
    # set a variable that will call whatever column
    # we want to visualise on the map
    variable = 'deces'
    # set range for the choropleth
    vmin = together['deces'].min()
    vmax = together['deces'].max()
    # create figure and axes
    fig, ax = plt.subplots(1, figsize=(16, 7))
    # create map
    together.plot(column=variable,
                  cmap=('Reds'),
                  linewidth=0.8,
                  ax=ax,
                  edgecolor='0.6')
    # remove the axis
    ax.axis('off')
    # add a title
    # make it correspond to the granularity!
    ax.set_title('Actual number of death per {}'.format(gra),
                 fontdict={'fontsize': '25',
                           'fontweight': '4'})
    # create colorbar as a legend
    sm = plt.cm.ScalarMappable(
        cmap='Reds',
        norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig.colorbar(sm)
    fig.savefig('toto.svg')


# vizmap('departement')
