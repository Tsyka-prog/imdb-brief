import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to browse all pages to scrape
def get_pages(url):
    pages = []
    for i in range(1, 250, 50):
        next_url = url + str(i) + '&ref_=adv_nxt'
        pages.append(next_url)
    return pages


# Function to scrape and create the dataframe
def movies_scrap (pages) :
    movies_df = pd.DataFrame(columns=['ranking', 'title', 'year', 'type', 'rating', 'runtime', 'directors', 'stars', 'votes','gross'])
    final_df = pd.DataFrame(columns=['ranking', 'title', 'year', 'type', 'rating', 'runtime', 'directors', 'stars', 'votes','gross'])
    
    for i in range(len(pages)):
        url = pages[i]
        response = requests.get(url)
        
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            datas = soup.find_all('div', class_="lister-item-content")
            
            for index, data in enumerate(datas):
                try:
                    movies_df.at[index, 'ranking'] = data.find(class_='lister-item-index').get_text().strip('.')
                    movies_df.at[index, 'title'] = data.h3.a.get_text()
                    movies_df.at[index, 'year'] = data.find(class_='lister-item-year').get_text().strip('(I) ()')
                    movies_df.at[index, 'type'] = data.find(class_='genre').get_text().strip('\n ').split(', ')
                    movies_df.at[index, 'rating'] = data.find(class_='ratings-bar').strong.get_text()
                    movies_df.at[index, 'runtime'] = data.find(class_='runtime').get_text().strip(' min')
                    directors_ls = [director_name for director_name in data.find('p', class_="").stripped_strings if director_name != ',']
                    directors_ls = directors_ls[1:directors_ls.index('|')]
                    movies_df.at[index, 'directors'] = directors_ls 
                    
                    stars_ls = [star_name for star_name in data.find('p', class_="").stripped_strings if star_name != ',']
                    stars_ls = stars_ls[stars_ls.index('|')+2:]
                    movies_df.at[index, 'stars'] = stars_ls   
                    movies_df.at[index, 'votes'] = data.find('p', class_='sort-num_votes-visible').contents[3].attrs['data-value']
                    
                    
                    movies_df.at[index, 'gross'] = data.find('p', class_='sort-num_votes-visible').contents[9].attrs['data-value'].replace(',', '')                
                except IndexError:
                    continue
                    
        final_df = pd.concat([final_df, movies_df], ignore_index=True)
        final_df['ranking'] = final_df['ranking'].astype(int)
        final_df['year'] = final_df['year'].astype(int)
        final_df['rating'] = final_df['rating'].astype(float)
        final_df['runtime'] = final_df['runtime'].astype(int)
        final_df['votes'] = final_df['votes'].astype(int)
        final_df['gross'] = final_df['gross'].astype(float)
    return final_df