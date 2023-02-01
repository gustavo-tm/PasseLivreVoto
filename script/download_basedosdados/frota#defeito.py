import pandas as pd
from pathlib import Path
import basedosdados as bd

path = str(Path(__file__).resolve().parents[2])

def download():
    query = '''
    SELECT *
    FROM `basedosdados.br_denatran_frota.municipio_tipo` 
    WHERE ano = 2021 AND mes = 1
    LIMIT 10000
    '''
    
    frota = bd.read_sql(query, billing_project_id="python-371123")
    frota.to_csv(path+"/input/tidy/frota.csv")