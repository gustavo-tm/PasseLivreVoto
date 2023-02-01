import pandas as pd
from pathlib import Path
import unidecode as uc

path = str(Path(__file__).resolve().parents[2])

def tidy():
    abst_1t = (pd.read_excel(path+"/input/raw/abstencao_1t.xlsx").query("nm_pais == 'Brasil'")
               .rename({"qt_eleitor_abstencao": "abstencao_1t_qt", "sg_uf":"uf"}, axis = 1)
               .drop(["aa_eleicao", "nm_pais", "nm_regiao", "qt_eleitor_comp"], axis = 1))
    abst_2t = (pd.read_excel(path+"/input/raw/abstencao_2t.xlsx").query("nm_pais == 'Brasil'")
               .rename({"qt_eleitor_abstencao": "abstencao_2t_qt", "sg_uf":"uf"}, axis = 1)
               .drop(["aa_eleicao", "nm_pais", "nm_regiao", "qt_eleitor_comp"], axis = 1))
                       
    abst = (pd.merge(abst_1t, abst_2t, on = ["nm_municipio", "uf", "qt_eleitor_apto"])
            .assign(nm_municipio = lambda _: 
                        _.nm_municipio.apply(lambda __: 
                                                 uc.unidecode(__.upper())))
           .replace({'nm_municipio' : { '-' : " ", "D'OESTE":"DO OESTE", "TERESINHA": "TEREZINHA",
                                       "IZABEL": "ISABEL"}}, regex = True)
           .replace({'nm_municipio' : { '-' : " ", "AREZ": "ARES", "CAMACANRI": "CAMACARI", "CAMACA": "CAMACAN",
                                       "ASSU": "ACU", "BOA SAUDE": "JANUARIO CICCO (BOA SAUDE)",
                                       "FLORINEA": "FLORINIA", "ELDORADO DOS CARAJAS": "ELDORADO DO CARAJAS",
                                       "GRACCHO CARDOSO": "GRACHO CARDOSO", "TABOCAO": "FORTALEZA DO TABOCAO",
                                       "MUQUEM DO SAO FRANCISCO": "MUQUEM DE SAO FRANCISCO",
                                       "SAO CAITANO": "SAO CAETANO", "SAO LUIS DO PARAITINGA": "SAO LUIZ DO PARAITINGA"}}))
    
    municipios = (pd.read_csv(path+"/input/tidy/municipios.csv")
                   .filter(["id_municipio", "nm_municipio", "uf"]))
    
    (pd.merge(abst, municipios, on = ["nm_municipio", "uf"],how = "right")
     .drop(["nm_municipio", "uf"], axis = 1)
     .to_csv(path+"/input/tidy/abstencao.csv"))