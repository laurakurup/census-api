# Census API Python Script

This script creates a pandas dataframe and csv file from the U.S. Census Decennial Census API, which offers access to population data by sex, age, race, etc. and housing data by occupancy, vacancy status, and tenure. 

In a few quick steps, you'll be querying to your heart's content.


## 1) Request a Census API key

It's easy!  And fast! Request at [http://www.census.gov/developers/](http://www.census.gov/developers/)


## 2) Identify variables

You need a [csv file](https://github.com/laurakurup/census-api/raw/master/census_variables.csv) of the variables you want to gather.  It should look like this:

| year | variable | column_name    |
|------|----------|----------------|
| 2010 | H0110004 | housing_renter |
| 2000 | H011003  | housing_renter |

[**Download the template:** https://github.com/laurakurup/census-api/raw/master/census_variables.csv](https://github.com/laurakurup/census-api/raw/master/census_variables.csv).

The template has extra columns, which cut and paste nicely from the Census variable reference pages (links below). **Extra columns are ignored by the script**.  Feel free to delete them!  Or add more!  The script only references _year_, _variable_ and _column_name_.  

#### API Limits?
You can run this script for 1 variable or hundreds of variables!  The script will divide your requests into batches of 50 (the API limit) and run multiple requests to gather your data.


#### Find variables by year:

+ 2010 Census: http://api.census.gov/data/2010/sf1/variables.html

+ 2000 Census: http://api.census.gov/data/2000/sf1/variables.html 
 
Make sure you list the correct year for each variable.  The variables change year to year, even for the same data.

#### Customize your column names:

In your [csv file](https://github.com/laurakurup/census-api/raw/master/census_variables.csv) file, provide the name you want for each column of data.  Don't need human-readable column names?  You can simply cut/paste the variables into this column.  

If 'add_year'is True (line 73), **the script adds the year to the column name**:

year:_2000_ column_name:_housing_renter_ becomes _housing_renter_2000_

year:_2010_ column_name:_housing_renter_ becomes _housing_renter_2010_    


## 3) Locations:

You have options!  This script can gather data for 4 types of locations:

+ **'state'** returns data for 50 U.S. States 
+ **'county'** returns data for 3,142 counties in U.S. States
+ **'metro'** returns data for 685 metropolitan areas (50,000+ population) in the U.S.
+ **'metro-micro'** returns metro plus 564 micropolitan areas (10,000 - 50,000 population)

Source files and documentation available here: [https://github.com/laurakurup/data](https://github.com/laurakurup/data)

You may get a few errors since cities and counties have formed, merged, dissolved, etc. These data files work well for 2010 and 2000 with only a handful of inconsistencies.  The script prints errors so you'll see what doesn't work.  If you want to query 1990, you may want to find FIPS codes that were accurate for 1990. For more info, see [https://www.census.gov/geo/reference/county-changes.html](https://www.census.gov/geo/reference/county-changes.html).    





