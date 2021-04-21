# ---------- requirements ----------
from datetime import datetime, timedelta
import os


# ---------- preprocess functions ----------

def map_save_path_routine(file_path):
    if (file_path == '~/Desktop/vizcovidfr_files/'):
        A = os.path.expanduser("~")
        B = "Desktop"
        file_path = os.path.join(A, B)

    if not os.path.exists(os.path.join(file_path, "vizcovidfr_files")):
        os.mkdir(os.path.join(file_path, "vizcovidfr_files"))

    file_path = os.path.join(file_path, "vizcovidfr_files")
    return file_path
