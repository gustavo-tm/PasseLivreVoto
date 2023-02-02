import pandas as pd
import zipfile
import glob

def tidy():
    df = (
        pd.read_csv("input/raw/municipios_brasileiros_tse.csv")
        .filter(["codigo_tse", "codigo_ibge"])
        .rename({"codigo_ibge": "id_municipio"}, axis = 1)
    )

    for file in glob.glob("input/raw/TSE/*"):
        with zipfile.ZipFile(file) as z:
            print(file)
            with z.open(file[14:-4] + ".csv") as f:
                print(z, f)
                df = (pd.read_csv(f, encoding= "latin", sep = ";")
                    .filter(["NR_TURNO", "ANO_ELEICAO", "CD_MUNICIPIO", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCAO"])
                    .groupby(by = ["NR_TURNO", "CD_MUNICIPIO", "ANO_ELEICAO"])
                    .sum()
                    .unstack(level = [0, 2])
                    .T
                    .reset_index()
                    .rename({"level_0": "variavel"}, axis = 1)
                    .assign(coluna = lambda _: _.variavel.str.lower() + "_" + _.NR_TURNO.astype(str) + "t" + "_" + _.ANO_ELEICAO.astype(str))
                    .set_index("coluna")
                    .drop(["variavel", "NR_TURNO", "ANO_ELEICAO"], axis = 1).T.reset_index().rename_axis("", axis = 1)
                    .rename({"CD_MUNICIPIO": "codigo_tse"}, axis = 1)
                    .merge(df, on = "codigo_tse")
                    )
    df.to_csv("input/tidy/abstencao.csv")