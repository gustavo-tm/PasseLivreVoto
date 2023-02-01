import pandas as pd
from pathlib import Path
import basedosdados as bd

path = str(Path(__file__).resolve().parents[2])

def download():
    query = '''
    SELECT id_municipio, pib, va_agropecuaria, va_industria, 
           va_servicos, va_adespss 
    FROM `basedosdados.br_ibge_pib.municipio` 
    WHERE ano = 2019
    LIMIT 10000
    '''
    
    pib = bd.read_sql(query, billing_project_id="python-371123")
    pib.to_csv(path+"/input/tidy/pib.csv")
