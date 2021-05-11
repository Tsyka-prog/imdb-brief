import pandas as pd 
import pickle

#scrapping lib
import requests
from bs4 import BeautifulSoup
#from lxml import html

from sklearn.preprocessing import MultiLabelBinarizer

def request_url(i):
    """ to be completed """
    url= f'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start={i}&ref_=adv_nxt'
    page_response=requests.get(url,timeout=5)
    soup =BeautifulSoup(page_response.content, 'html.parser')
    datas=soup.find_all('div', class_="lister-item-content")
    return datas

def scrapping_web_page(datas, movies_df):
    """ method scrapping the web page, this method returns a single dataframe """
    
    for index, data in enumerate(datas):
        movies_df.loc[index, 'Ranking'] = data.find(
            class_='lister-item-index unbold text-primary').get_text().strip('.')
        # inside data, we look in 'h3' tag then display the text inside 'a' tag
        movies_df.at[index, 'Title'] = data.h3.a.get_text()
        # .at method allows us to pass a list into a single value
        movies_df.at[index, 'Genre'] = data.find(class_='genre').get_text().strip('\n ').split(", ")
        movies_df.at[index, 'Year'] = data.find(class_='lister-item-year').get_text().strip('(I) ()')
        movies_df.at[index, 'Runtime_min'] = int(data.find(class_='runtime').get_text().strip('min'))
        movies_df.at[index, 'Rating'] = float(data.find(class_='ratings-bar').strong.get_text())
        #scrapping of directors & actors list 
        team_list = [team_name for team_name in data.find('p', class_='').stripped_strings if team_name != ',']
        directors_list = team_list[1:team_list.index('|')]
        stars_list = team_list[team_list.index('|')+2:]
        movies_df.at[index, 'Directors'] = directors_list
        movies_df.at[index, 'Stars'] = str(stars_list)
        # captures valeurs non trouvables sur le site
        try:
            # we look in 'p' tag called sort-num_votes-visible, display all child info inside the p tag
            # (contents returned a list of children),
            # votes are in third posision in the list returned by contents
            # attrs return a dictionary of the data of contents[3] thanks to that we target the 'data-value' key
            movies_df.at[index, 'Votes'] = int(data.find('p', class_='sort-num_votes-visible').contents[3].attrs['data-value'])
            movies_df.at[index, 'Gross'] = int(data.find('p', class_='sort-num_votes-visible').contents[9].attrs['data-value'].replace(',', ''))
        except IndexError:
            continue
        # last_classment=movies_df.iloc[index]['classment']
    return(movies_df)

def save_data(final_df):
    final_df.to_pickle('scrapping_imdb.pkl')