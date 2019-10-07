#Find restaurants near Case Western Reserve University baesd on Rating
import requests
def get_businesses(query,api_key,min_rating=0.0,max_results = 30):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s" % (query,api_key)
    response = requests.get(url)
    data = response.json()['results']
    while 'next_page_token' in response.json().keys():
        #Get next page token
        pagetoken = response.json()['next_page_token']
        new_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=%s&pagetoken=%s" % (api_key,pagetoken)
        response = requests.get(new_url)
        while response.json().get('status') != 'OK':
            from time import sleep
            from random import random
            sleep(random())
            response = requests.get(new_url)
        data = data + response.json()['results']    
        results = [None]*len(data)
        for i in range(len(data)):
            if data[i]['rating'] >= min_rating:
                name = data[i]['name']
                location = data[i]['formatted_address']
                open_status = data[i]['opening_hours']
                rating = data[i]['rating']
                if 'price_level' not in data[i].keys() :
                    price = None
                else:
                    price = data[i]['price_level']
            results[i] = (name, location, open_status, price, rating)
        results2 = results.copy()
        if len(results2) > max_results:
            results2 = results2[0:max_results]
        if len(results2) <= max_results:
            break
    
    return results2

#Find restaurant near Case Western Reserve University which rating greater than 4.0
# Your API key
api_key = '****'
query = "restaurants+near+Case+Western+Reserve+University"
get_businesses(query,api_key,min_rating=4)
