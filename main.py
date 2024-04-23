import os
import serpapi
import pandas as pd

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)


reviews = []  # empty list which will hold dictionaries of reviews
i = 0

next_page_token = ""

switch = True
while switch:

    results = client.search({
        'engine': 'google_maps_reviews',
        'type': 'search',
        'data_id': '0x3ae2fc0237ed5d25:0x4c711f0161ac8139',
        'next_page_token': next_page_token

    })

    print(results['reviews'])

    for i in range(len(results['reviews'])):
        result = results['reviews'][i]
        if result.get('rating'):
            rating = result['rating']
        if result.get('date'):
            date = result['date']
        if result.get('snippet'):
            snippet = result['snippet']
        if result.get('review_id'):
            review_id = result['review_id']
        reviews.append({'review_id': review_id,
                        'date': date,
                        'snippet': snippet,
                        'rating': rating, })

    if results.get("serpapi_pagination") and results.get("serpapi_pagination").get("next") and results.get(
            "serpapi_pagination").get("next_page_token"):
        next_page_token = results['serpapi_pagination']['next_page_token']
    else:
        switch = False

df = pd.DataFrame(reviews)
print(df)

df.to_csv("google_reviews.csv", sep=',', index=False, encoding='utf-8')
