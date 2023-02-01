import pandas as pd
import numpy as np
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])

def tidy():
    eleicao_governador = pd.read_excel(path+"/input/raw/eleicao_governador.xlsx")
    
    municipios = pd.read_csv(path+"/input/tidy/municipios.csv").filter(["uf", "id_municipio"])
    
    (eleicao_governador
     .rename({"2T (S/N)": "eleicao_gov_2t", "UF": "uf"}, axis = 1)
     .filter(["eleicao_gov_2t", "uf"])
     .merge(municipios, on = "uf", how = "right")
     .assign(eleicao_gov_2t = lambda _: np.where(_.eleicao_gov_2t == "SIM", 1, 0))
     .drop("uf", axis = 1)).to_csv(path+"/input/tidy/eleicao_governador.csv")