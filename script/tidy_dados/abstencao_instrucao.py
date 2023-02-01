import pandas as pd
import numpy as np
import unidecode as uc
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])

def tidy():
    municipios = pd.read_csv(path+"/input/tidy/municipios.csv").filter(["nm_municipio","uf", "id_municipio"])
    
    abstencao_instrucao_1t = (pd.read_excel(path+"/input/raw/abstencao_instrucao_1t.xlsx").query("nm_pais == 'Brasil'")
               .assign(abstencao_1t_pct = lambda _: _.qt_eleitor_abstencao/_.qt_eleitor_apto)
               .rename({"qt_eleitor_abstencao": "abstencao_1t_qt", "sg_uf":"uf", 
                        "ds_grau_escolaridade": "instrucao"}, axis = 1)
               .drop(["aa_eleicao", "nm_pais", "nm_regiao", "qt_eleitor_comp", "abstencao_1t_qt"], axis = 1))
    
    abstencao_instrucao_2t = (pd.read_excel(path+"/input/raw/abstencao_instrucao_2t.xlsx").query("nm_pais == 'Brasil'")
               .assign(abstencao_2t_pct = lambda _: _.qt_eleitor_abstencao/_.qt_eleitor_apto)
               .rename({"qt_eleitor_abstencao": "abstencao_2t_qt", "sg_uf":"uf", 
                        "ds_grau_escolaridade": "instrucao"}, axis = 1)
               .drop(["aa_eleicao", "nm_pais", "nm_regiao", "qt_eleitor_comp", "abstencao_2t_qt"], axis = 1))
    
    abstencao_instrucao = (pd.merge(abstencao_instrucao_1t, abstencao_instrucao_2t, 
                                    on = ["nm_municipio", "uf", "qt_eleitor_apto", "instrucao"])
                .assign(nm_municipio = lambda _: 
                            _.nm_municipio.apply(lambda __: 
                                                     uc.unidecode(__.upper())),
                       instrucao = lambda _: _.instrucao.str.lower())
               .replace({'nm_municipio' : { '-' : " ", "D'OESTE":"DO OESTE", "TERESINHA": "TEREZINHA",
                                           "IZABEL": "ISABEL"},
                         'instrucao':{" ": "_"}}, regex = True)
               .replace({'nm_municipio' : { '-' : " ", "AREZ": "ARES", "CAMACANRI": "CAMACARI", "CAMACA": "CAMACAN",
                                           "ASSU": "ACU", "BOA SAUDE": "JANUARIO CICCO (BOA SAUDE)",
                                           "FLORINEA": "FLORINIA", "ELDORADO DOS CARAJAS": "ELDORADO DO CARAJAS",
                                           "GRACCHO CARDOSO": "GRACHO CARDOSO", "TABOCAO": "FORTALEZA DO TABOCAO",
                                           "MUQUEM DO SAO FRANCISCO": "MUQUEM DE SAO FRANCISCO",
                                           "SAO CAITANO": "SAO CAETANO", "SAO LUIS DO PARAITINGA": "SAO LUIZ DO PARAITINGA"}}))
    
    (pd.merge(abstencao_instrucao, municipios, on = ["nm_municipio", "uf"],how = "right")
     .drop(["nm_municipio", "uf"], axis = 1)
     .pivot_table(columns = ["instrucao"], 
                  values = ["qt_eleitor_apto", "abstencao_1t_pct", "abstencao_2t_pct"], 
                  index = "id_municipio").unstack().reset_index()
     .assign(var = lambda _: _.level_0 + "_" + _.instrucao)
     .filter([0, "var", "id_municipio"])
     .rename({0: "valor"}, axis = 1)
     .set_index("var")
     .pivot_table(columns = ["var"], 
                  values = ["valor"], 
                  index = "id_municipio")
    )["valor"].reset_index().rename_axis("", axis='columns').to_csv(path+"/input/tidy/abstencao_instrucao.csv")