import glob
import pandas as pd
import numpy as np
import re
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])

def tidy():
    #Importa e arruma os dados de cada estação meteorológica 
    def organizar_estacoes():
        
        files = [file for file in glob.glob(path+"/input/raw/meteorologia/*") 
                 if re.search('A_31-10-2022.CSV$', file)]
        
        dados_estacoes = pd.DataFrame()
        for file in files:
            header = (pd.read_csv(file, sep = ";", encoding="latin", on_bad_lines='skip', nrows=7)
                        .set_index("REGIAO:").T)
        
            df = (pd.read_csv(file, sep = ";", encoding="latin", on_bad_lines='skip', skiprows=8)
                    .rename({"Hora UTC": "hora", "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)": "precipitacao",
                                "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)": "temp",
                                "UMIDADE RELATIVA DO AR, HORARIA (%)": "umidade"}, axis = 1)
                    .assign(hora = lambda _: _.hora.apply(lambda __: int(__.split(" ")[0][0:2])+3))
                    .query("(Data == '2022/10/02' or Data == '2022/10/31') and hora >= 8 and hora <= 17")
                    .filter(["Data","hora","temp","precipitacao", "umidade"])
                    .replace(",", ".", regex = True)
                    .replace({"2022/10/02": "1t", "2022/10/31": "2t"})
                    .assign(temp = lambda _: pd.to_numeric(_.temp),
                            precipitacao_mm = lambda _: pd.to_numeric(_.precipitacao),
                            precipitacao_hr = lambda _: pd.to_numeric(_.precipitacao),
                            umidade = lambda _: pd.to_numeric(_.umidade),
                            unidade = lambda _: 1)
                    .groupby(by= "Data").aggregate({"temp":"mean", "umidade": "mean","unidade": "max", "precipitacao_mm": "sum",
                                                    "precipitacao_hr": lambda _: np.mean(np.where(_ > 0,1,0))})
                    .reset_index().pivot_table(columns = ["Data"], 
                                                values = ["precipitacao_mm", "precipitacao_hr", "temp", "umidade"], 
                                                index = "unidade")
                    .unstack().reset_index()
                    .assign(obs = lambda _: _.level_0 + "_" + _.Data)
                    .filter([0, "obs"])
                    .set_index("obs").T
                    .assign(lat = float(header["LATITUDE:"].replace(",", ".", regex = True)),
                        long = float(header["LONGITUDE:"].replace(",", ".", regex = True)),
                        estacao = header["ESTACAO:"].to_string()))
            
            dados_estacoes = pd.concat([dados_estacoes, df])
        dados_estacoes = dados_estacoes.rename_axis("", axis = 1).reset_index(drop = True)
        return dados_estacoes
    
    
    #Atribui a cada município os dados da estação mais próxima
    def cruzar_mun():

        dados_estacoes = organizar_estacoes()
        
        #Conversão de latitude e longitude para radianos
        dados_estacoes = (dados_estacoes
            .assign(lat_rad = lambda _: np.deg2rad(_.lat),
                    long_rad = lambda _: np.deg2rad(_.long))
        )

        municipios = (pd.read_csv(path + "/input/raw/municipios.csv")
            .filter(["codigo_ibge","latitude", "longitude"])
            .assign(lat_rad = lambda _: np.deg2rad(_.latitude),
                    long_rad = lambda _: np.deg2rad(_.longitude))
        )

        #Coordenadas das estações
        coords = list(dados_estacoes.assign(coord = lambda _: list(zip(_.lat_rad, _.long_rad))).coord)
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', metric="haversine").fit(coords)

        #Coordenadas dos municípios
        coords = list(municipios.assign(coord = lambda _: list(zip(_.lat_rad, _.long_rad))).coord)
        distances, indices = nbrs.kneighbors(coords)

        meteorologia = (
            pd.concat(
                [municipios,
                pd.DataFrame(distances, columns = ["distancia"]),
                pd.DataFrame(indices, columns = ["NN"])],
                axis = 1
            )
            .assign(distancia = lambda _: _.distancia * 6371)#radianos para metros
            .merge(dados_estacoes, left_on = "NN", right_index= True, how = "left")
            .filter(["codigo_ibge", "precipitacao_mm_1t", "precipitacao_mm_2t"])
            .rename({"codigo_ibge": "id_municipio"}, axis = 1)
            )
        print(meteorologia.columns)
        return meteorologia
    
    cruzar_mun().to_csv(path+"/input/tidy/meteorologia.csv")
