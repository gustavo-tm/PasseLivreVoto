import pandas as pd
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])

def tidy():
    frota = (pd.read_excel(path+"/input/raw/frota.xls", skiprows = 2)
             .rename({"MUNICIPIO": "nm_municipio"}, axis = 1))
    frota.columns = [coluna.lower() for coluna in frota.columns]
    
    municipios = (pd.read_csv(path+"/input/tidy/municipios.csv")
                  .filter(["id_municipio", "nm_municipio", "uf"]))
    
    (pd.merge(municipios, frota, 
              on = ["nm_municipio", "uf"], how = "left")
     .drop(["nm_municipio", "uf"], axis = 1)
     .to_csv(path+"/input/tidy/frota.csv"))
