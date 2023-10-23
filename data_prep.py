#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:18:16 2020

@author: jeremy
"""

import requests
import pandas as pd
import os
from dateutil.parser import parse
from sklearn.impute import SimpleImputer

# url of data source
csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"

# # this block downloads the above csv and saves it in the current directory
req = requests.get(csv_url)
url_content = req.content
csv_file = open('downloaded.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

# df = pd.read_csv (r'Path where the CSV file is stored\File name.csv')

df = pd.read_csv(os.getcwd()+'/updated_us_time_series_data.csv')

wisc = df.loc[df['Province_State'] == 'Wisconsin']
wisc = wisc.drop(["UID", "iso2", "iso3","code3","FIPS","Province_State","Country_Region","Lat","Long_","Combined_Key"], axis = 1)
wisc.to_csv(os.getcwd()+'/wisconsin_time_series_data.csv')

df = df.loc[df['sub_region_1'] == 'Wisconsin']
df.to_csv(os.getcwd()+'/wisconsin_mobility_data.csv')

########

state = pd.read_csv(os.getcwd()+'/wisconsin_time_series_data.csv')
mobility = pd.read_csv(os.getcwd()+'/wisconsin_mobility_data.csv')

counts = []

i = 0
while i < len(mobility):
    date_array = parse(mobility.loc[i][1])
    date = '%s/%s/%s' % (date_array.month, date_array.day, str(date_array.year)[-2:])
    
    county = ' '.join(mobility.loc[i][0].split()[:-1])
    counts.append(state.loc[state['Admin2'] == county].iloc[0].get(date))
    i = i + 1

se = pd.Series(counts)
mobility['infection_count'] = se.values
mobility.to_csv(os.getcwd()+'/wisconsin_mobility_data_with_counts.csv')
df = pd.read_csv(os.getcwd()+'/wisconsin_mobility_data_with_counts.csv')
counties = list(set(df['sub_region_2'].tolist()))
test = df.loc[df['sub_region_2'] == counties[0]]

text = "retail_and_recreation_percent_change_from_baseline"
rural = []
urban = []
for name in counties:
    county_data = df.loc[df['sub_region_2'] == name]
    percent_empty = round(county_data["residential_percent_change_from_baseline"].isnull().mean()*100,2)
    
    if percent_empty < 10:
        urban.append(name)
    else:
        rural.append(name)
        
df = pd.read_csv(os.getcwd()+'/urban_wisconsin_mobility_data_with_counts.csv')
df = df.drop(["Unnamed: 0", "Unnamed: 0.1","parks_percent_change_from_baseline", "transit_stations_percent_change_from_baseline"], axis = 1)

test = df.loc[df['date'] == '2020-08-18']

dates = list(set(df['date'].tolist()))

for day in dates:
    temp = df.loc[df['date'] == day]
    imr = SimpleImputer()
    imr = imr.fit(temp.iloc[:,2:].values)
    imputed_data = imr.transform(temp.iloc[:,2:].values)
    temp2 = temp.iloc[:,2:]
    temp2[:] = imputed_data
    df.update(temp2)

df.to_csv(os.getcwd()+'/imputed_urban_wisconsin_mobility_data_with_counts.csv', index=False)