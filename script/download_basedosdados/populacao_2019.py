import pandas as pd
from pathlib import Path
import basedosdados as bd

path = str(Path(__file__).resolve().parents[2])

def download():
    query = '''
    SELECT id_municipio, populacao as populacao_2019
    FROM `basedosdados.br_ibge_populacao.municipio` 
    WHERE ano = 2019
    LIMIT 10000
    '''
    
    pop = bd.read_sql(query, billing_project_id="python-371123")
    pop.to_csv(path+"/input/tidy/populacao_2019.csv")