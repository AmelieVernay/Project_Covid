from download import download
import pandas as pd
import os

url = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
path_target = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "chiffres-cles.csv")

class Load_chiffres_cles:
    def __init__(self, url=url, target_name=path_target):
        download(url, target_name, replace=True)
        # above, set replace to True to always get the updated version

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target)
        return df

url2 = "https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-stocks-des-doses-de-vaccins-contre-la-covid-19/#_"
path_target2 = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data", "./stocks-es-national.csv")

class Load_Vaccine_storage:
    def __init__(self, url=url2, target_name=path_target2):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target2)
        return df

