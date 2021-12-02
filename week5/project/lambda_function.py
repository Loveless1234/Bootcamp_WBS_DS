
import pandas as pd
import numpy as np
import requests
import mysql.connector
import json
import unicodedata
import re
import bs4
from bs4 import BeautifulSoup as bs




def lambda_handler(event, context):
    # connect to database
    schema="gans"
    host="wbs-project3-db.cvojr846itjc.us-east-2.rds.amazonaws.com"
    user="admin"
    password="Jaanu123"
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
    
    
    city = "Berlin"
    country = "DE"
    OWM_key = "0b72d424f8aa757bc21cb2a396aba540"
    # achieve the same result with the wather api
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast/?q={city},{country}&appid={OWM_key}&units=metric&lang=en')
    
    forecast_api = response.json()['list']
    # look for the fields that could ve relevant: 
    # better field descriptions https://www.weatherbit.io/api/weather-forecast-5-day

    weather_info = []

    # datetime, temperature, wind, prob_perc, rain_qty, snow = [], [], [], [], [], []
    for forecast_3h in forecast_api: 
        weather_hour = {}
        # datetime utc
        weather_hour['datetime'] = forecast_3h['dt_txt']
        # temperature 
        weather_hour['temperature'] = forecast_3h['main']['temp']
        # wind
        weather_hour['wind'] = forecast_3h['wind']['speed']
        # probability precipitation 
        try: weather_hour['prob_perc'] = float(forecast_3h['pop'])
        except: weather_hour['prob_perc'] = 0
        # rain
        try: weather_hour['rain_qty'] = float(forecast_3h['rain']['3h'])
        except: weather_hour['rain_qty'] = 0
        # wind 
        try: weather_hour['snow'] = float(forecast_3h['snow']['3h'])
        except: weather_hour['snow'] = 0
        weather_hour['municipality_iso_country'] = city + ',' + country
        weather_info.append(weather_hour)
    
    weather_data = pd.DataFrame(weather_info)
 
    
    weather_data.assign(datetime = lambda x: pd.to_datetime(x['datetime'])).to_sql('weathers', if_exists='append', con=con, index=False)
    
     #Flight Api
    airport_icoa = "EDDB"
    to_local_time = "2021-10-04T20:00"
    from_local_time = "2021-10-05T08:00"
    
    url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{airport_icoa}/{to_local_time}/{from_local_time}"
    
    querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"false","withLocation":"false"}
    
    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': "8f9f83bab9msh9cbc143b90ebf53p169e3ejsn9597fff30d82"
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    arrivals_berlin = response.json()['arrivals']
    
    
    
    def get_flight_info(flight_json):
        # terminal
        try: terminal = flight_json['arrival']['terminal']
        except: terminal = None
        # aircraft
        try: aircraft = flight_json['aircraft']['model']
        except: aircraft = None
    
        return {
            'dep_airport':flight_json['departure']['airport']['name'],
            'sched_arr_loc_time':flight_json['arrival']['scheduledTimeLocal'],
            'terminal':terminal,
            'status':flight_json['status'],
            'aircraft':aircraft,
            'icao_code':airport_icoa
        }

    
   
    arrivals_berlin = pd.DataFrame([get_flight_info(flight) for flight in arrivals_berlin])
    
    (
    arrivals_berlin
    .replace({np.nan},'unknown')
    .assign(sched_arr_loc_time = lambda x: pd.to_datetime(x['sched_arr_loc_time']))
    .to_sql('arrivals', if_exists='append', con=con, index=False))
    
    
    
    
      
    #cities = ['Berlin', 'Hamburg', 'Frankfurt','Munich','Stuttgart','Leipzig','Cologne','Dresden','Hannover','Paris', 'Barcelona','Lisbon','Madrid']
    cities = ['Berlin','Paris','Amsterdam','Barcelona','Rome','Lisbon','Prague','Vienna','Madrid']

    def City_info(soup):
        
        ret_dict = {}
        ret_dict['city'] = soup.h1.get_text()
        
        
        if soup.select_one('.mergedrow:-soup-contains("Mayor")>.infobox-label') != None:
            i = soup.select_one('.mergedrow:-soup-contains("Mayor")>.infobox-label')
            mayor_name_html = i.find_next_sibling()
            mayor_name = unicodedata.normalize('NFKD',mayor_name_html.get_text())
            ret_dict['mayor']  = mayor_name
        
        if soup.select_one('.mergedrow:-soup-contains("City")>.infobox-label') != None:
            j =  soup.select_one('.mergedrow:-soup-contains("City")>.infobox-label')
            area = j.find_next_sibling('td').get_text()
            ret_dict['city_size'] = unicodedata.normalize('NFKD',area)
    
        if soup.select_one('.mergedtoprow:-soup-contains("Elevation")>.infobox-data') != None:
            k = soup.select_one('.mergedtoprow:-soup-contains("Elevation")>.infobox-data')
            elevation_html = k.get_text()
            ret_dict['elevation'] = unicodedata.normalize('NFKD',elevation_html)
        
        if soup.select_one('.mergedtoprow:-soup-contains("Population")') != None:
            l = soup.select_one('.mergedtoprow:-soup-contains("Population")')
            c_pop = l.findNext('td').get_text()
            ret_dict['city_population'] = c_pop
        
        if soup.select_one('.infobox-label>[title^=Urban]') != None:
            m = soup.select_one('.infobox-label>[title^=Urban]')
            u_pop = m.findNext('td')
            ret_dict['urban_population'] = u_pop.get_text()
    
        if soup.select_one('.infobox-label>[title^=Metro]') != None:
            n = soup.select_one('.infobox-label>[title^=Metro]')
            m_pop = n.findNext('td')
            ret_dict['metro_population'] = m_pop.get_text()
        
        if soup.select_one('.latitude') != None:
            o = soup.select_one('.latitude')
            ret_dict['lat'] = o.get_text()
            
        if soup.select_one('.longitude') != None:    
            p = soup.select_one('.longitude')
            ret_dict['longit'] = p.get_text()
    
        
        return ret_dict



    list_of_city_info = []
    for city in cities:
        url = 'https://en.wikipedia.org/wiki/{}'.format(city)
        web = requests.get(url,'html.parser')
        soup = bs(web.content)
        list_of_city_info.append(City_info(soup))
    df = pd.DataFrame(list_of_city_info)
    df.to_sql('df_cities', if_exists='append', con=con, index=False)
    

    



