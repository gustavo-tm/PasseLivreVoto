import glob
import pandas as pd
import json

df = pd.read_csv("input/tidy/municipios.csv", index_col=0)

for base in [base for base in glob.glob("input/tidy/*") if base != "input/tidy\\municipios.csv"]:
    print(base)
    df = pd.merge(df, pd.read_csv(base, index_col=0), on = "id_municipio", how = "left")

dicionario = json.loads(open("script/variaveis_calculadas.txt").read())

df = (df
    .filter(json.loads(open("script/variaveis.txt").read()).keys())
    .assign(**{key: eval(value[0]) for key, value in dicionario.items()})
    .drop(list(set(sum([delete[1] for delete in list(dicionario.values())], []))), axis =1)
    )


df.to_csv("output/base.csv")
df.to_excel("output/base.xlsx")