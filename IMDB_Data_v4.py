import requests
import bs4
from requests import get
from bs4 import BeautifulSoup
from time import sleep # sleep timer 
from time import time
from random import randint # used for timer
from IPython.core.display import clear_output # used to clear output of frequency test
import warnings


#empty lists to fill.
names = []
years = []
imdb_ratings = []
meta_scores = []
genres = []
lengths = []
descriptions = []
votes = []
movie_no = 0

start_time = time()
requests = 0

pages = [str(i) for i in range(1,10)]
years_url = [str(i) for i in range(1990,2020)]
headers = {"Accept-Language": "en-US, en;q=0.5"}

#Loop through years 1990-2020
for year_url in years_url:
    resultsnumber =1
      
    #loop through pages
    for page in pages: 
        
        #make request to page
        response = get('https://www.imdb.com/search/title?release_date=' + year_url +
                       "&sort=num_votes,desc&start=" + str(resultsnumber) + "&ref_=adv_nxt")
        print('https://www.imdb.com/search/title?release_date=' + year_url +
                       "&sort=num_votes,desc&start=" + str(resultsnumber) + "&ref_=adv_nxt")
        resultsnumber += 50
    
        #pause loop random interval 8-15
        sleep(randint(8,15))
        
        #monitor requests
        requests += 1
        elapsed_time = time () - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)
        
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
        
        #parse request to beautiful soup
        page_html = BeautifulSoup(response.text, 'html.parser')
        
        #select all movie containers
        movie_containers = page_html.findAll("div", {"class": "lister-item mode-advanced"})
        print(movie_containers[0].h3.a.text)
    
        for container in movie_containers:
            #the name
            film_Name = container.h3.a.text
            names.append(film_Name)
            
            #the year
            year = container.h3.find("span", {"class":"lister-item-year text-muted unbold"}).text
            years.append(year)
            #the imdb rating    
            imdb_Rating = float(container.strong.text)
            imdb_ratings.append(imdb_Rating)
            #the metascore rating    
            if container.find("span", {"class":"metascore favorable"}) is not None:
                meta_Score = container.find("span", {"class":"metascore favorable"}).text
            else:
                meta_Score = "no metascore"
            meta_scores.append(meta_Score.strip())
            #the genres   
            genre = container.find("span", {"class":"genre"}).text.strip()
            genres.append(genre)
            #the length rating 
            if container.find("span", {"class":"runtime"}) is not None:
                length = container.find("span", {"class":"runtime"}).text.strip()
                
            else: 
                length = "no length"
            lengths.append(length)   
            #the description    
            description = container.findAll("p")[1].text.strip()
            descriptions.append(description)
            #the no votes  
            no_Votes = int(container.find("span", {'name':'nv'})['data-value'])
            votes.append(int(no_Votes))
   
    
# import pandas and turn into table
import pandas as pd
movie_table = pd.DataFrame({"Movie": names, "Year": years , 
                        "IMDB Rating": imdb_ratings , "Votes": votes,  
                        "MetaScore":  meta_scores, "Genres": genres, 
                        "lengths": lengths, "Description": descriptions})
print(movie_table.info())
movie_table.to_csv("IMDB_filmList.csv")