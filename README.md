# Census API Python Script

This script creates a pandas dataframe and csv file from the U.S. Census Decennial Census API, which offers access to population data by sex, age, race, etc. and housing data by occupancy, vacancy status, and tenure. 

In a few quick steps, you'll be querying to your heart's content.


## 1) Request a Census API key

It's easy!  And fast! Request at [http://www.census.gov/developers/](http://www.census.gov/developers/)

## 2) Identify variables

**Get the csv template:** [https://github.com/laurakurup/census-api/raw/master/census_variables.csv](https://github.com/laurakurup/census-api/raw/master/census_variables.csv)

Variables can be found here:

+ 2010 Census: http://api.census.gov/data/2010/sf1/variables.html

+ 2000 Census: http://api.census.gov/data/2000/sf1/variables.html 

#### Customize your column names

In the [census_variables.csv](https://github.com/laurakurup/census-api/raw/master/census_variables.csv) file, provide the name you want for each column of data.  Don't need human-readable column names?  You can simple cut/paste the variables.  

If **'add_year'** is True (line 73), the script adds the year to the column name:

year:**'2000'** column_name:**'housing_renter'** becomes **'housing_renter_2000'**

year:**'2010'** column_name:**'housing_renter'** becomes **'housing_renter_2010'**    

#### Only the first three columns are used by this script. 

The label and concept columns are option.  They can be ignored or used for your reference.  I use them to track the census explinations for each variable.  Add more columns if you want!  Just make sure the first three columns are year, variable and column_name.

Make sure you list the correct year for each variable.  They change year to year, even for the same data.  For example:

| year | variable | column_name    | label           | concept                                     |
|------|----------|----------------|-----------------|---------------------------------------------------------------
| 2010 | H0110004 | housing_renter | Renter occupied | H11. TOTAL POPULATION IN OCCUPIED... | 
| 2000 | H011003  | housing_renter | Renter occupied | H11. Total Population In Occupied... | 

...  if you query 2010 for H011003, you'll get an error.


## 3) Locations:

You have options!  This script can gather data for 4 types of locations:

+ **'state'** returns data for 50 U.S. States 
+ **'county'** returns data for 3,142 counties in U.S. States
+ **'metro'** returns data for 685 metropolitan areas (50,000+ population) in the U.S.
+ **'metro-micro'** returns metro plus 564 micropolitan areas (10,000 - 50,000 population)

Source files and documentation available here: [https://github.com/laurakurup/data](https://github.com/laurakurup/data)

You may get a few errors since cities and counties have formed, merged, dissolved, etc. These data files work well for 2010 and 2000.  If you want to query 1990, you may want to find FIPS codes that were accurate for 1990. For more info, see [https://www.census.gov/geo/reference/county-changes.html](https://www.census.gov/geo/reference/county-changes.html).    





