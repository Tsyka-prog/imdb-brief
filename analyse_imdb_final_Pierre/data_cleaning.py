import pandas as pd
import numpy as np

#petit code de nettoyage des données Stars
def clean_stars(final_df):
    final_df['Stars']=final_df['Stars'].map(lambda x: x.lstrip('[').rstrip(']'))
    final_df['Stars']=final_df['Stars'].replace({'\'': ''}, regex=True)
    for i, v in enumerate(final_df['Stars']):
        final_df.at[i,'Stars']=v.split(',')
    return(final_df)

def une_colonne_par_liste(final_df):    
    final_df=pd.concat([final_df['Stars'].apply(pd.Series),final_df],axis=1)
    final_df=final_df.rename(columns={0: "Stars_1", 1: "Stars_2", 2:"Stars_3",3:"Stars_4"})
    final_df=pd.concat([final_df['Genre'].apply(pd.Series),final_df],axis=1)
    final_df=final_df.rename(columns={0: "Genre_1", 1: "Genre_2", 2:"Genre_3"})
    final_df=pd.concat([final_df['Directors'].apply(pd.Series),final_df],axis=1)
    final_df=final_df.rename(columns={0: "Director_1", 1: "Director_2", 2:"Director_3"})
    final_df=final_df.drop(['Directors','Stars','Genre'],axis=1)
    return(final_df)

def regroup_by_decade(final_df):
    #creation of a 10 years bins 
    bins = pd.IntervalIndex.from_tuples([(1920, 1930), (1930, 1940), (1940, 1950),
                                    (1950, 1960), (1960, 1970), (1970, 1980),
                                    (1980, 1990), (1990, 2000), (2000, 2010), (2010, 2020)])

    final_df[['Decenie']] = pd.cut(np.array(final_df['Year']), bins)
    #final_df[['Decenie']] = pd.cut(np.array(final_df['Year']),11,labels=[1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2020])
    #aggregate groupby on decades
    total_by_decades = final_df.groupby(by=['Decenie'], as_index=False).agg({'Title':'count','Votes':'mean','Rating':'mean'})
    total_by_decades=total_by_decades.rename(columns={'Title': "Number_of_movies", 'Votes': "Average_nb_of_votes", 'Rating':"Average_ratings"}).round(decimals=2)
    return(total_by_decades)
