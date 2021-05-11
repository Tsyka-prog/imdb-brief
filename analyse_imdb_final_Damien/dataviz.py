import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
from pandas_profiling import ProfileReport
from sklearn.preprocessing import MultiLabelBinarizer

# Matrice de corrélation
def matrix_correlation(imdb):
    corr = imdb.corr()
    # Génération d'un masque pour le triangle supérieur droit
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Generation d'une cmap
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    # Dessin de la heatmap avec ses options
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, square=True, cbar_kws={"shrink": .75}, annot=True).set_title('Map de corrélation', size=15)
    
    
# Regplot montrant la corrélation entre les votes et les notes
def regplot_votes_rating(imdb):
    plt.figure(figsize=(8,6))
    sns.regplot(data=imdb, x="rating", y="votes");


# Barplot du nb de films dans le top 250 en fonction de la décennie
def total_by_decade(imdb):
    total_par_an = imdb.groupby('decade').agg({'title': 'count'})
    plt.figure(figsize=(8,6))
    sns.barplot(data=total_par_an, x=total_par_an.index, y='title').set(xlabel="Décennies", ylabel = "Nb de films", title="Nombre de films dans le top 250 en fonction des decennies")


# Barplot moyenne des recettes par rapport aux notes
def barplot_gross_rating(imdb): 
    plt.figure(figsize=(8, 6))
    sns.barplot(data=imdb, x='rating', y='gross', capsize=.2).set_title('Moyenne des recettes par rapport à la note', size=15)
    

# Utilisation de la fonction MultiLabaleBinarizer() - SkLearn - afin de récupérer chaque élément de la liste se trouvant dans la série "type"
def types_movies(imdb):
    type_mlb = imdb['type']
    mlb = MultiLabelBinarizer()
    movies_types = pd.DataFrame(mlb.fit_transform(type_mlb),columns=mlb.classes_, index=imdb.index).sum()
    movies_types
    movies_types.sort_values(ascending=False)
    # Treemap des différents genre de films
    plt.figure(figsize=(12,8))
    squarify.plot(sizes=movies_types, label=movies_types.index, alpha=.6).set_title('Treemap des différents genres de films', size=15)