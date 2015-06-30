'''
Last Updated June 30, 2015
by Laura Kurup
https://github.com/laurakurup

Create a pandas dataframe and csv file from the U.S. Census Decennial 
Census API, which offers access to population data by sex, age, race, 
etc. and housing data by occupancy, vacancy status, and tenure.             


Census API key:

    Request at http://www.census.gov/developers/
        
Variables:

    Get the csv template: 
    https://github.com/laurakurup/census-api/raw/master/census_variables_sample.csv
    
    ... and fill it in with the variables you want! Only the first three 
    columns are used by this script.  The remaining columns can be ignored 
    or used for your reference.  Variables can be found here:
    
    Variables for 2010 Census:
    http://api.census.gov/data/2010/sf1/variables.html
            
    Variables for 2000 Census:  
    http://api.census.gov/data/2000/sf1/variables.html 
    
Column Names:

    In the csv file, provide the name you want for each column of data.  If 
    'add_year' is True (line 73), the script adds the year to the column name:
    
    year:'2000' column_name:'housing_renter' becomes 'housing_renter_2000'
    
    year:'2010' column_name:'housing_renter' becomes 'housing_renter_2010'    

Locations:

    'state' returns data for 50 U.S. States 
    'county' returns data for 3,142 counties in U.S. States
    'metro' returns data for 685 metropolitan areas (50,000+ population) in the U.S.
    'metro-micro' returns metro plus 564 micropolitan areas (10,000 - 50,000 population)
    
    Source files and documentation available here: https://github.com/laurakurup/data 
    
    You will see a few errors since cities and counties have formed, merged, 
    dissolved, etc. These data files work well for 2010 and 2000.  If you want 
    to query 1990, you may want to find FIPS codes that were accurate for 1990.
    For more info, see https://www.census.gov/geo/reference/county-changes.html.    
                 
                                                                            '''
      
                               
                               
''' Configure your request '''

# census API key --> request at http://www.census.gov/developers/
census_api_key = 'YOUR-KEY-HERE'

# csv file of the variables you want (relative path from python's working directory)
# Get the template: https://github.com/laurakurup/census-api/raw/master/census_variables_sample.csv
variables_csv = 'census_variables.csv'

# 'state', 'county', 'metro' or 'metro-micro'
location_type = 'state'   

# maximum variables per request
api_variable_limit = 50

# want to add the year to the end of your column names? (True or False)
add_year = True

# subdirectory for data exports (relative to python's working directory)
# if not using, leave as empty string
subdirectory = 'data/census/'

# want to add a timestamp to the end of your csv filename?  True / False
# this keeps me from overwriting my data :)
time_stamp = True




''' Imports '''

import pandas as pd
import urllib2
import datetime
import time


''' Process your variables '''

# read in the data
df = pd.read_csv(variables_csv)

# creates a list of dictionaries from relevant columns
variables_list = df[['year', 'variable', 'column_name']].to_dict(orient='records')

# create a list of the years to query (must be seperate API calls)
years_to_query = [item for item in set([item['year'] for item in variables_list])]


''' Set up the dataframe based on location type '''

# create a dataframe of the lcation names and FIPS codes
if location_type == 'metro' or location_type == 'metro-micro': 
    fips_codes = 'https://github.com/laurakurup/data/raw/master/us_metro_areas/us_metro_areas_fips_codes.csv'
    df = pd.read_csv(fips_codes, dtype={'state_fips': object, 'place_fips': object})
elif location_type == 'state': 
    fips_codes = 'https://raw.githubusercontent.com/laurakurup/data/master/us_states/us_states_fips_codes.csv'
    df = pd.read_csv(fips_codes, dtype={'state_fips': object})
else: 
    fips_codes = 'https://github.com/laurakurup/data/raw/master/us_counties/us_counties_fips_codes.csv'
    df = pd.read_csv(fips_codes, dtype={'state_fips': object, 'county_fips': object})

# if 'metro' only, drop the micropolitan areas, leaving the 685 metropolitan areas
if location_type == 'metro':    
    df = df[df['metro_micro'] != 'micropolitan']
    df = df.reset_index(drop=True)


''' Optional: Test your query '''

# save some time! uncomment line 124 to cut your request to 10 locations
# if everything is running smoothly, rerun it on the full list  :)
# df = df.head(10)


''' Get the data  '''

# function that will request and save the data for each source URL
def get_census_data(source_url):
    # start timing the request
    start_time = time.time()
    # print location to be requested
    if location_type == 'state':
        print "requesting data for " + source_url.split('=')[3] + ' . . .'
    else:
        print "requesting data for " + source_url.split('=')[4].split('&')[0] + ' ' + source_url.split('=')[3].split('&')[0] + ' . . .'
    try:
        # read json for the source URL
        response = pd.read_json(source_url)
        # transpose for easy saving
        response = response.transpose()
        # if location type is state, save all but the last value (the state FIPS)
        if location_type == 'state':
            data = [item for item in response[1]][:-1]
        # otherwise, save all but the last two values (the state and place FIPS)
        else:
            data = [item for item in response[1]][:-2]
        # print a success message with the length of time
        print("success! %s seconds" % (round(time.time() - start_time, 5)))
        print '---------------------------------------------------'
    # If the API returns a HTTPError, print the error message and the source URL
    except urllib2.HTTPError, error:
        contents = error.read()
        print 'ERROR MESSAGE FROM API: ' + contents
        print source_url
        print '---------------------------------------------------'
        # save 'error' for the variables requested
        data = ['error'] * len(source_url.split(','))
    # For other errors, print the source URL
    # this will happen if the location does not exist for the year requested
    except:
        print 'ERROR – NO RESPONSE FOR URL:'
        print source_url
        print '---------------------------------------------------'
        # save 'error' for the variables requested
        data = ['error'] * len(source_url.split(','))
    # return a list of the response values
    return data

# to build the source URLs, iterate through each year
for year in years_to_query:
    # create a list of the variables for the year
    new_variables_list = [item for item in variables_list if item['year'] == year]
    # iterate through list(s) of variables that are < the api limit
    for i in xrange(i, len(new_variables_list), api_variable_limit):
        print 'Starting request for Census ' + str(year) + ' variables ' + str(i) + ' through ' + str(i+api_variable_limit) + ':'
        print '---------------------------------------------------'
        # create a list of the next batch of varibles to request
        list_within_limit = new_variables_list[i:i+api_variable_limit]
        # create a string of variables to build the source URL (comma seperated, no spaces)
        variables_str = ''
        for item in list_within_limit:
            variables_str = variables_str + item['variable'] + ','
        # trim the last character (extra comma)
        variables_str = variables_str[:-1]
        # build the source URL based on location type
        if location_type == 'metro' or location_type == 'metro-micro': 
            df['source_url'] = 'http://api.census.gov/data/' + str(year) + '/sf1?key=' + census_api_key + '&get=' + variables_str + '&for=place:' + df['place_fips'] + '&in=state:' + df['state_fips']
        elif location_type == 'state':
            df['source_url'] = 'http://api.census.gov/data/' + str(year) + '/sf1?key=' + census_api_key + '&get=' + variables_str + '&for=state:' + df['state_fips']
        else: 
            df['source_url'] = 'http://api.census.gov/data/' + str(year) + '/sf1?key=' + census_api_key + '&get=' + variables_str + '&for=county:' + df['county_fips'] + '&in=state:' + df['state_fips']       
        # run the get_census_data() function on each source URL, create a new column of results
        df['new_data'] = [get_census_data(item) for item in df['source_url']]
        print 'Request complete for Census ' + str(year) + ' variables ' + str(i) + ' through ' + str(i+api_variable_limit)
        print '---------------------------------------------------'
        # iterate through the list of variables that were requested to create columns
        for item in list_within_limit:
            # create column names for each variable with the year (if add_year == True)
            if add_year == True:
                new_column_name = item['column_name'] + '_' + str(item['year'])
            # create column names for each variable without the year (if add_year == False)
            else:
                new_column_name = item['column_name']
            # create the new column with the data returned from the API
            n = list_within_limit.index(item)
            df[new_column_name] = [item[n] for item in df['new_data']]  
    # print success message when year is complete
# print success message when everything is complete
print 'FINISHED! Request complete for all ' + str(len(variables_list)) + ' variables'


''' Clean up and export to csv'''

# drop unneeded columns (used during API calls)
df = df.drop('source_url', 1)
df = df.drop('new_data', 1)

# construct csv file name with date and time added to file name (if time_stamp == True)
if time_stamp == True:
    file_name = subdirectory + 'census-data-by-' + location_type + '-' + datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d-%I.%M%p') + '.csv'
# construct csv file name without date and time (if time_stamp == False)
else: 
    file_name = subdirectory + 'census-data-by' + location_type + '.csv'

# save data to csv    
df.to_csv(file_name, index=False)   


