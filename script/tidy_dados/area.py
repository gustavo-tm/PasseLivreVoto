import pandas as pd
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])

def tidy():
    area = (pd.read_excel(path+"/input/raw/area.xls", nrows = 5572)
              .filter(["AR_MUN_2021", "CD_MUN"])
              .rename({"AR_MUN_2021": "area", "CD_MUN": "id_municipio"}, axis = 1)
              .assign(id_municipio = lambda _: _.id_municipio.astype(str)))
    area.to_csv(path+"/input/tidy/area.csv")


