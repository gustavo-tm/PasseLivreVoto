import pandas as pd
from pathlib import Path
import basedosdados as bd

path = str(Path(__file__).resolve().parents[2])

def download():
    query = '''
    SELECT id_municipio, ideb
    FROM `basedosdados.br_inep_ideb.municipio` 
    WHERE ano = 2019 AND rede = 'publica'
    LIMIT 20000
    '''
    
    ideb = bd.read_sql(query, billing_project_id="python-371123")
    ideb = ideb.groupby(by = "id_municipio").mean().reset_index()
    ideb.to_csv(path+"/input/tidy/ideb.csv")
