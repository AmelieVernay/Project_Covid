# ---------- requirements ----------

from vizcovidfr.loads import load_datasets

# load 'stocks_es_national' dataset
df_vaccine_storage = load_datasets.Load_Vaccine_storage().save_as_df()
