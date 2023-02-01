import pandas as pd
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])

def tidy():
    passe_livre = (pd.read_excel(path+"/input/raw/passe_livre.xlsx")
                      .assign(passe_livre = lambda _: 1)
                      .drop(["Cidade", "Estado", "População"], axis = 1)
                      .rename({"Início": "passe_livre_inicio", "Código IBGE": "id_municipio"}, axis = 1))

    municipios = (pd.read_csv(path+"/input/tidy/municipios.csv")
                  .filter(["id_municipio"]))

    passe_livre = (pd.merge(passe_livre, municipios, on = "id_municipio", how = "right")
                   .assign(passe_livre = lambda _: _.passe_livre.fillna(0)))
    
    passe_livre.to_csv(path+"/input/tidy/passe_livre.csv")
    
