from download import download
import pandas as pd
import os
from datetime import date


# Define global path target on which to join our files.
# Ends up in the data folder
path_target = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                "..", "data")

# ---------- chiffres-cles ----------
url_cc = "https://www.data.gouv.fr/en/datasets/r/0b66ca39-1623-4d9c-83ad-5434b7f9e2a4"
path_target_cc = os.path.join(path_target, "chiffres-cles.csv")


class Load_chiffres_cles:
    """
    Download and save 'chiffres-cles.csv',
    a dataset containing general Covid-19 informations
    """
    def __init__(self, url=url_cc, target_name=path_target_cc):
        download(url, target_name, replace=True)
        # above, set replace to True to always get the updated version

    @staticmethod
    def save_as_df():
        # convert last lines type to str to avoid DtypeWarning
        converters = {'source_nom': str, 'source_url': str,
                      'source_archive': str, 'source_type': str}
        df_covid = pd.read_csv(path_target_cc, converters=converters)
        return df_covid


# ---------- transfer ----------
url_tr = "https://www.data.gouv.fr/fr/datasets/r/70cf1fd0-60b3-4584-b261-63fb2281359e"
path_target_tr = os.path.join(path_target, "transfer.csv")


class Load_transfer:
    """
    Download and save 'transfer.csv',
    a dataset containing informations about Covid-19 patient transfers
    """
    def __init__(self, url=url_tr, target_name=path_target_tr):
        download(url, target_name, replace=True)
        # above, set replace to True to always get the updated version

    @staticmethod
    def save_as_df():
        df_tr = pd.read_csv(path_target_tr)
        return df_tr


# ---------- stocks-es-national ----------
url_sen = "https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-stocks-des-doses-de-vaccins-contre-la-covid-19/#_"
path_target_sen = os.path.join(path_target, "./stocks-es-national.csv")


class Load_Vaccine_storage:
    """
    Download and save 'stocks-es-national.csv',
    a dataset containing Covid-19 vaccination informations
    """
    def __init__(self, url=url_sen, target_name=path_target_sen):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target_sen)
        return df


# ---------- chiffres-fr ----------
url_cfr = "https://www.data.gouv.fr/fr/datasets/r/d3a98a30-893f-47f7-96c5-2f4bcaaa0d71"
path_target_cfr = os.path.join(path_target, "./chiffres-fr.csv")


class Load_chiffres_fr:
    """
    Download and save 'chiffres-fr.csv',
    a dataset containing ???
    """
    def __init__(self, url=url_cfr, target_name=path_target_cfr):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df_covid = pd.read_csv(path_target_cfr)
        return df_covid


# ---------- posquotreg ----------
url_posreg = "https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01"
path_target_posreg = os.path.join(path_target, "./posquotreg.csv")


class Load_posquotreg:
    """
    Download and save 'posquotreg.csv',
    a dataset containing ???
    """
    def __init__(self, url=url_posreg, target_name=path_target_posreg):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target_posreg, sep=";")
        return df


# ---------- posquotdep ----------
url_posdep = "https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675"
path_target_posdep = os.path.join(path_target, "./posquotdep.csv")


class Load_posquotdep:
    """
    Download and save 'posquotdep.csv',
    a dataset containing ???
    """
    def __init__(self, url=url_posdep, target_name=path_target_posdep):
        download(url, target_name, replace=True)

    @staticmethod
    def save_as_df():
        df = pd.read_csv(path_target5, sep=";")
        return df
