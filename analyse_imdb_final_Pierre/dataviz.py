#dataviz lib
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import pandas as pd 
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer


def graph_square(final_df):
    type_mlb = final_df['Genre']
    mlb = MultiLabelBinarizer()
    movies_types = pd.DataFrame(mlb.fit_transform(type_mlb),columns=mlb.classes_, index=final_df.index).sum()
    movies_types.sort_values(ascending=False)
    plt.figure(figsize=(12,8))
    squarify.plot(sizes=movies_types, label=movies_types.index, alpha=.8 )
    plt.title('Les genres présents dans le top 250 IMDB')
    #plt.axis('off')
    return(plt.show())


def top_5(user_choice, final_df):
    if user_choice == 1:
        type_mlb = final_df['Stars']
        mlb = MultiLabelBinarizer()
        movies_stars = pd.DataFrame(mlb.fit_transform(type_mlb),columns=mlb.classes_, index=final_df.index).sum()
        #movies_stars= movies_stars.sort_values(ascending=False)
        #movies_stars=[movies_stars[movies_stars> 3]]
        data={'stars':movies_stars.index, 'nb_films':movies_stars}
        movies_stars=pd.DataFrame(data=data)
        movies_stars.sort_values(by=['nb_films'],ascending=False, inplace=True)
        result=sns.barplot(data=movies_stars.head(10),y='stars',x='nb_films' );
    elif user_choice == 2 : 
        type_mlb = final_df['Directors']
        mlb = MultiLabelBinarizer()
        movies_directors = pd.DataFrame(mlb.fit_transform(type_mlb),columns=mlb.classes_, index=final_df.index).sum()
        #movies_directors=movies_directors.sort_values(ascending=False)
        #movies_directors = [movies_directors[movies_directors >4]]
        data={'directors':movies_directors.index, 'nb_films':movies_directors}
        movies_directors=pd.DataFrame(data=data)
        movies_directors.sort_values(by=['nb_films'], ascending=False, inplace=True)
        result=sns.barplot(data=movies_directors.head(10),y='directors',x='nb_films');
    elif user_choice ==3 :
        type_mlb = final_df['Genre']
        mlb = MultiLabelBinarizer()
        movies_types = pd.DataFrame(mlb.fit_transform(type_mlb),columns=mlb.classes_, index=final_df.index).sum()
        #movies_types= movies_types.sort_values(ascending=False)
        data={'genres':movies_types.index, 'nb_films':movies_types}
        movies_types=pd.DataFrame(data=data)
        movies_types.sort_values(by=['nb_films'], ascending=False, inplace=True)
        result=sns.barplot(data=movies_types.head(10),y='genres',x='nb_films');
    return(result)


def corr_matrice(final_df):
    # calculate the correlation matrix
    corr = final_df.corr()
    mask=np.triu(np.ones_like(corr,dtype=bool))
    # plot the heatmap
    plt.title('Matrice de Corrélation')
    return(sns.heatmap(corr, 
            xticklabels=corr.columns,
            yticklabels=corr.columns, annot=True, mask=mask ))

