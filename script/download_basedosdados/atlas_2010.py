import pandas as pd
from pathlib import Path
import basedosdados as bd

path = str(Path(__file__).resolve().parents[2])

def download():
    query = '''
    SELECT populacao as populacao_2010, * 
    FROM `basedosdados.mundo_onu_adh.municipio` 
    WHERE ano = 2010
    LIMIT 10000
    '''
    
    atlas = bd.read_sql(query, billing_project_id="python-371123")
    atlas.to_csv(path+"/input/tidy/atlas.csv")