import pandas as pd
from pathlib import Path
import unidecode as uc
import numpy as np

path = str(Path(__file__).resolve().parents[2])

def tidy():
    passe_livre_eleicao = (pd.read_excel(path+"/input/raw/passe_livre_eleicao.xlsx", skiprows = 2)
                             .rename({"Unnamed: 0": "indx", "1º Turno": "passe_livre_1t", 
                                      "2º Turno": "passe_livre_2t", "UF": "uf"}, axis = 1)
                             .query("indx <=394")
                             .filter(["Cidade", "uf", "passe_livre_1t", "passe_livre_2t"])
                             .assign(passe_livre_1t = lambda _: np.where(_.passe_livre_1t == "S", 1, 0),
                                     passe_livre_2t = lambda _: np.where(_.passe_livre_2t == "S", 1, 0),
                                     nm_municipio = lambda _: _.Cidade.apply(lambda __: uc.unidecode(__.upper())))
                            .drop("Cidade", axis = 1))
    
    municipios = (pd.read_csv(path+"/input/tidy/municipios.csv")
                  .filter(["id_municipio", "nm_municipio", "uf"]))
    
    (pd.merge(municipios, passe_livre_eleicao, 
              on = ["nm_municipio", "uf"], how = "left")
     .assign(passe_livre_1t = lambda _: _.passe_livre_1t.fillna(0),
             passe_livre_2t = lambda _: _.passe_livre_2t.fillna(0))
     .filter(["id_municipio", "passe_livre_1t", "passe_livre_2t"])
     .to_csv(path+"/input/tidy/passe_livre_eleicao.csv"))
    