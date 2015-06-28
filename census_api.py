'''
Created on Sat Jun 27, 2015
by Laura Kurup
https://github.com/laurakurup

Create a pandas dataframe and csv file from the U.S. Census Decennial 
Census API, which offers access to population data by sex, age, race, 
etc. and housing data by occupancy, vacancy status, and tenure. 


1) REQUEST A CENSUS API KEY

        request at http://www.census.gov/developers/

2) IDENTIFY WHICH VARIABLES AND YEAR

        variables for 2010 Census:
        http://api.census.gov/data/2010/sf1/variables.html
        
        variables for 2000 Census:  
        http://api.census.gov/data/2000/sf1/variables.html
        
3) SELECT WHICH TYPE OF LOCATION

        'county' returns data for 3142 counties in U.S. States and Territories
        'metro' returns data for 685 metropolitan areas (50,000 + population) in the U.S.
        'metro-micro' returns data for metropolitan areas plus 564 micropolitan areas (10,000 - 50,000 population)
        
'''



''' Configure your request '''

# census API key --> 
census_api_key = 'YOUR-KEY-HERE'

# variable(s) to download (limit of 50)
get_variables = ['PCT0050002', 'PCT0060002', 'PCT0070002']  

# '1990', '2000' or '2010'
census_year = '2010'   

# 'county', 'metro' or 'metro-micro'
location_type = 'metro'   




''' Get your data '''

# imports
import pandas as pd
import time

# create a dataframe of the FIPS codes
if location_type == 'metro' or location_type == 'metro-micro': 
    fips_codes = 'https://github.com/laurakurup/census-api/raw/master/us_metro_areas_fips_codes.csv'
    df = pd.read_csv(fips_codes, dtype={'state_fips': object, 'place_fips': object})
else: 
    fips_codes = 'https://github.com/laurakurup/census-api/raw/master/us_counties_fips_codes.csv'
    df = pd.read_csv(fips_codes, dtype={'state_fips': object, 'county_fips': object})

if location_type == 'metro':    
    # drop the micropolitan areas, leaving the 685 metropolitan areas
    df = df[df['metro_micro'] != 'micropolitan']
    
# count the number of variables requested, format as a string for the API
variables_len = len(get_variables)
variables_str = ''
for item in get_variables:
    variables_str = variables_str + item + ','
variables_str = variables_str[:-1]

if location_type == 'metro' or location_type == 'metro-micro': 
    df['source_url'] = 'http://api.census.gov/data/' + census_year + '/sf1?key=' + census_api_key + '&get=' + variables_str + '&for=place:' + df['place_fips'] + '&in=state:' + df['state_fips']
else: 
    df['source_url'] = 'http://api.census.gov/data/' + census_year + '/sf1?key=' + census_api_key + '&get=' + variables_str + '&for=county:' + df['county_fips'] + '&in=state:' + df['state_fips']

# function to request the data for each FIPS code
# prints a status update for each call (success, error, time to complete)
# don't want all those updates? Comment out lines 85 - 88 and line 92
def get_census_data(source_url):
    try:
        start_time = time.time()
        place = source_url.split('=')[3].split('&')[0]
        state = source_url.split('=')[4].split('&')[0]
        print "requesting data for " + state + ' ' + place + ' . . .'
        response = pd.read_json(source_url)
        response = response.transpose()
        data = [item for item in response[1]][:-2]
        print("success! %s seconds" % (round(time.time() - start_time, 5)))
    except:
        data = 'error'
        print 'ERROR'
    return data

# query the API for your data!
df['data'] = [get_census_data(item) for item in df['source_url']]





''' Review Errors '''

# print the number of errors and identify the specific places
errors = str(len(df[df['data'] == 'error']['data']))
if errors == '0':
    print 'No errors!'
else:
    print ' --- ERROR: Unable to get data for ' + errors + ' locations --- '
    if location_type == 'metro' or location_type == 'metro-micro': 
        print df[df['data'] == 'error']['cbsa_name']
    else: 
        print df[df['data'] == 'error'][['state','county']]


# OPTIONAL: try again on the rows that returned an error
df[df['data'] == 'error']['data'] = [get_census_data(item) for item in df[df['data'] == 'error']['source_url']]

# OPTIONAL: drop the rows with errors
# df = df[df['data'] != 'error']



''' Format your new data '''

# create new columns for each variable with data
i = 0
while i < variables_len:
    df[get_variables[i]] = [item if item == 'error' else item[i] for item in df['data']]
    i = i + 1

# OPTIONAL: drop the source url and initial data columns 
df = df.drop('source_url', 1)
df = df.drop('data', 1)



''' Export to csv '''

# OPTIONAL --> subdirectory for data exports within python's working directory
# if not using, leave as empty string
subdirectory = 'data/census/'

# export file to csv
if location_type == 'metro' or location_type == 'metro-micro': 
    file_name = subdirectory + 'census-' + census_year + '-data-export-by-metro.csv'
else: 
    file_name = subdirectory + 'census-' + census_year + '-data-export-by-county.csv'

df.to_csv(file_name, index=False)   
