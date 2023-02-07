import json
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

# INPUT FILTERS YOUR CAR

print("If you don't know what type just skip 'Enter' ")
filter_enum_make = input('Maker: (Toyota, Audi, Volvo) \n').lower()
filter_enum_model = input('Model: \n').lower()
filter_enum_body_type = input('Body type: (sedan, combi, cabrio, coupe, compact, suw) \n')
filter_enum_fuel_type = input('Fuel type: (petrol, diesel, petrol-lpg, hybrid) \n')
filter_enum_gearbox = input("Gearbox type: (automatic or manual) \n")
filter_enum_door_count = input('Door count: (5 or 3)  \n')
filter_float_year_from = input('Year from: \n')
filter_float_year_to = input('Year to: \n')
filter_float_mileage_from = input('Min mileage: \n')
filter_float_mileage_to = input('Max mileage \n')
print(filter_enum_make.upper(), filter_enum_model.upper(), ',',
      filter_enum_body_type.upper(), filter_enum_door_count, 'doors', ',',
      filter_enum_gearbox, ',',
      'Type fuel:', filter_enum_fuel_type, ',',
      'Year:', filter_float_year_from, '-', filter_float_year_to, ',',
      'Mileage:', filter_float_mileage_from, '-', filter_float_mileage_to)

# MAKE JSON FOR REQUESTS POST

variables_0 = {
  "includeFiltersCounters": True,
  "criteria": {
    "filters": [
      {
        "name": "category_id",
        "value": "29"
      },
      {
        "name": "filter_enum_make",
        "value": filter_enum_make
      },
      {
        "name": "filter_enum_model",
        "value": filter_enum_model
      },
      {
        "name": "filter_enum_fuel_type",
        "value": filter_enum_fuel_type
      },
      {
        "name": "filter_enum_damaged",
        "value": "0"
      },
      {
        "name": "filter_enum_body_type",
        "value": filter_enum_body_type
      },
      {
        "name": "filter_enum_door_count",
        "value": filter_enum_door_count
      },
      {
        "name": "filter_enum_registered",
        "value": "1"
      },
      {
        "name": "filter_float_year:from",
        "value": filter_float_year_from
      },
      {
        "name": "filter_float_year:to",
        "value": filter_float_year_to
      },
      {
        "name": "filter_float_mileage:from",
        "value": filter_float_mileage_from
      },
      {
        "name": "filter_float_mileage:to",
        "value": filter_float_mileage_to
      },
      {
        "name": "filter_enum_rhd",
        "value": "0"
      },
      {
        "name": "filter_enum_gearbox",
        "value": filter_enum_gearbox
      }
    ]
}
}
variables = json.dumps(variables_0, indent=2)
# print(variables)
headers = {'Content-type': 'application/json'}
query = """query getAdvertSearchSummary($criteria: AdvertSearchCriteria!, $includeFiltersCounters: Boolean!) {
  advertSearchSummary(criteria: $criteria) {
    url
    totalCount
    filtersCounters @include(if: $includeFiltersCounters) {
      name
      nodes {
        name
        value
        __typename
      }
      __typename
    }
    __typename
  }
}
"""
url = "https://www.otomoto.pl/graphql"
# REQUESTS POST WITH YOUR FILTERS
r = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
l = []
# print(r.status_code)
json_0 = r.text

json_1 = json.loads(json_0)
totalCount = (json_1['data']["advertSearchSummary"]['totalCount'])
webpage_0 = (json_1["data"]["advertSearchSummary"]['url'])
# GET A SEARCHING LINK
print(webpage_0)
# CREATE LINKS FOR NEXT PAGES
pages = np.arange(1, 10)
for page in pages:
    url_search = webpage_0 + "&page=" + str(page)+".html"
# SCRAPING
    r2 = requests.get(url_search)
    webpage = bs(r2.text)
    articles = webpage.main.select('article', attrs={'data-highlight': 'false'})
    for article in articles:
        id_offers = article.attrs['id']
        title = article.find('a').text
        price = article.find('span', class_='ooa-1bmnxg7').text.replace(' ', '').replace('PLN', '')
        price = int(price)
        rows = (id_offers, title, price)
        l.append(rows)
# CREATE A DATA FRAME
column_name = ["id", "Title", "Price"]
df = pd.DataFrame(l, columns=column_name)
df2 = df.drop_duplicates()
print(df2.sort_values("Price"))
print("Total " + str(totalCount) + ' PCS')


print("Min price " + str(df2['Price'].min()) + ' PLN')
print("Max price " + str(df2['Price'].max()) + ' PLN')
print("Median " + str(df2['Price'].median()) + ' PLN')
