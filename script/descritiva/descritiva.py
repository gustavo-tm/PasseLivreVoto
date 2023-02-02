from pathlib import Path
import pandas as pd
from plotnine import *
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from sklearn.manifold import MDS
from sklearn.cluster import KMeans

import warnings 

path = str(Path(__file__).resolve().parents[1])

df = pd.read_csv(path+"/output/base.csv", index_col=0)

def densidade():
    for variavel in df.columns:
        try:
            (ggplot(df)+geom_density(aes(variavel))).save(path+f"/output/descritiva/densidade/{variavel}.png", dpi = 300)
        except:
            print("error: "+variavel)

def mapear():
    distances = 1 - abs(
    df.drop("passe_livre_inicio", axis = 1).corr())

    mds = MDS(n_components = 2, dissimilarity = "precomputed").fit_transform(distances)
    coords = pd.DataFrame(dict(name = distances.index,
                             x1 = mds[:, 0],
                             x2 = mds[:, 1]))
    
    kmeans = KMeans(n_clusters = 10, n_init = 10000, random_state = 42).fit(coords[["x1", "x2"]])
    
    coords["cluster"] = kmeans.labels_
    
    (ggplot(coords, aes(x = "x1", y = "x2", label = "name", color = "cluster")) +
         geom_label(size = 12, alpha = .5) +
         scale_color_gradient(low = "blue", high = "red") +
         theme(figure_size = (15, 15), legend_position = "none") +
         labs(x = "", y = "")+
         xlim(-.8,.8)+
         ylim(-.8,.8)).save(path+"/output/descritiva/mapa.png", dpi=600)
    
    # warnings.filterwarnings("ignore")

    # twcd = [] # total within-clusters dispersion
    # for k in range(1, 10):
    #     kmeans = KMeans(n_clusters = k, random_state = 42).fit(coords[["x1", "x2"]])
    #     twcd.append(kmeans.inertia_)
        
    # (ggplot(None, aes(x = range(1, 10), y = twcd)) +
    #      geom_point(size = 1) +
    #      geom_line(color = "blue") +
    #      scale_x_continuous(breaks = range(1, 10)) +
    #      labs(x = "Number of clusters",
    #           y = "Total within-clusters dispersion",
    #           title = "Scree plot for k-means")).save(path+"/output/descritiva/twcd.png", dpi=600)

def corplot():
    #Matriz de covariância
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(df.corr(), mask=np.triu(np.ones_like(df.corr(), dtype=bool)), 
                cmap=sns.diverging_palette(230, 20, as_cmap=True), vmax=1, vmin = -1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    fig.savefig(path+"/output/descritiva/corrplot.svg", format='svg', dpi=1200)
    matplotlib.rcParams.update({'font.size': 2})

df.describe().T.to_excel(path+"/output/describe.xlsx")