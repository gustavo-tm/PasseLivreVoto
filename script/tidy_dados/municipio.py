import pandas as pd
from pathlib import Path
import unidecode as uc

path = str(Path(__file__).resolve().parents[2])

def tidy():
    mun = (pd.read_csv(path+"/input/raw/municipios.csv")
           .drop(["siafi_id", "ddd"], axis = 1)
           .rename({"nome": "nm_municipio", "codigo_ibge": "id_municipio", "sg_uf": "uf"}, axis = 1)
           .assign(nm_municipio = lambda _: 
                   _.nm_municipio.apply(lambda __: 
                                        uc.unidecode(__.upper())))
          .replace({'nm_municipio' : { '-' : " ", "D'OESTE":"DO OESTE", "TERESINHA": "TEREZININHA", "IZABEL": "ISABEL"}}, regex = True)
          .replace({"nm_municipio":{"SANTA TEREZININHA": "SANTA TEREZINHA", "AUGUSTO SEVERO (CAMPO GRANDE)": "CAMPO GRANDE"}}))
    
    
    est = (pd.read_csv(path+"/input/raw/estados.csv")
           .drop(["latitude", "longitude", "nome"], axis = 1))
    
    pd.merge(mun, est, on = ["codigo_uf"]).drop(["codigo_uf"], axis = 1).to_csv(path+"/input/tidy/municipios.csv")
