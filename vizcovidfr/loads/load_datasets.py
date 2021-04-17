from download import download
import pandas as pd
import os
from datetime import date


urlcc = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
path_target = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "chiffres-cles.csv")


class Load_chiffres_cles:
    def __init__(self, url=urlcc, target_name=path_target):
        download(url, target_name, replace=True)
        # above, set replace to True to always get the updated version

    @staticmethod
    def save_as_df():

        """
        Nicely formatted dataframe with time indexation.
        """
        # convert last lines type to str to avoid DtypeWarning
        converters = {'source_nom': str, 'source_url': str,
                      'source_archive': str, 'source_type': str}
        df_covid = pd.read_csv(path_target, converters=converters)
        return df_covid  # not have wrong data

url2 = "https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-stocks-des-doses-de-vaccins-contre-la-covid-19/#_"
path_target2 = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "./stocks-es-national.csv")


class Load_Vaccine_storage:
    def __init__(self, url=url2, target_name=path_target2):
        download(url2, path_target2, replace = True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target2)
        return df



url_cfr = "https://www.data.gouv.fr/fr/datasets/r/d3a98a30-893f-47f7-96c5-2f4bcaaa0d71"
path_target3 = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "./chiffres-fr.csv")


class Load_chiffres_fr:
    def __init__(self, url=url_cfr, target_name=path_target3):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():

        df_covid = pd.read_csv(path_target3)

        return df_covid


urlposreg = "https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
path_target4 = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "./posquotreg.csv")


class Load_posquotreg:
    def __init__(self, url=urlposreg, target_name=path_target):
        wget.download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target2, sep=";")
        return df

url_vac = "https://public.opendatasoft.com/explore/dataset/covid-19-france-vaccinations-age-sexe-dep/export/?disjunctive.variable_label&sort=date&refine.date=2021&refine.variable=Par+tranche+d%E2%80%99%C3%A2ge"
path_target5 = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "./covid-19-france-vaccinations-age-dep.csv")

class Load_vaccination:
    def __init__(self, url=url_vac, target_name=path_target5):
        download(url_vac, path_target5, replace=True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target5, sep=";")
        return df
