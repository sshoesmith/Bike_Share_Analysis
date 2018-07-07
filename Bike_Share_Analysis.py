
# coding: utf-8

# # 2016 US Bike Share Activity Snapshot
# 
# ## Table of Contents
# - [Introduction](#intro)
# - [Posing Questions](#pose_questions)
# - [Data Collection and Wrangling](#wrangling)
#   - [Condensing the Trip Data](#condensing)
# - [Exploratory Data Analysis](#eda)
#   - [Statistics](#statistics)
#   - [Visualizations](#visualizations)
# - [Performing Your Own Analysis](#eda_continued)
# - [Conclusions](#conclusions)
# 
# <a id='intro'></a>
# ## Introduction
# 
# 
# Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. Bicycle-sharing systems allow users to rent bicycles for short trips, typically 30 minutes or less. Thanks to the rise in information technologies, it is easy for a user of the system to access a dock within the system to unlock or return bicycles. These technologies also provide a wealth of data that can be used to explore how these bike-sharing systems are used.
# 
# In this project, I performed an exploratory analysis on data provided by [Motivate](https://www.motivateco.com/), a bike-share system provider for many major cities in the United States. I compared the system usage between three large cities: New York City, Chicago, and Washington, DC. I explored if there are any differences within each system for those users that are registered, regular users and those users that are short-term, casual users.

# # <a id='pose_questions'></a>
# ## Posing Questions
# 
# Before looking at the bike sharing data, you should start by asking questions you might want to understand about the bike share data. Consider, for example, if you were working for Motivate. What kinds of information would you want to know about in order to make smarter business decisions? If you were a user of the bike-share service, what factors might influence how you would want to use the service?
# 
# **Question 1**: Write at least two questions related to bike sharing that you think could be answered by data.
# 
# **Answer**: 
# 1. For how long on average are people renting the bikes? 
# 2. Is supply keeping up with demand?
# 
# 

# <a id='wrangling'></a>
# ## Data Collection and Wrangling
# 
# Now it's time to collect and explore our data. In this project, we will focus on the record of individual trips taken in 2016 from our selected cities: New York City, Chicago, and Washington, DC. Each of these cities has a page where we can freely download the trip data.:
# 
# - New York City (Citi Bike): [Link](https://www.citibikenyc.com/system-data)
# - Chicago (Divvy): [Link](https://www.divvybikes.com/system-data)
# - Washington, DC (Capital Bikeshare): [Link](https://www.capitalbikeshare.com/system-data)
# 
# If you visit these pages, you will notice that each city has a different way of delivering its data. Chicago updates with new data twice a year, Washington DC is quarterly, and New York City is monthly. **However, you do not need to download the data yourself.** The data has already been collected for you in the `/data/` folder of the project files. While the original data for 2016 is spread among multiple files for each city, the files in the `/data/` folder collect all of the trip data for the year into one file per city. Some data wrangling of inconsistencies in timestamp format within each city has already been performed for you. In addition, a random 2% sample of the original data is taken to make the exploration more manageable. 
# 
# **Question 2**: However, there is still a lot of data for us to investigate, so it's a good idea to start off by looking at one entry from each of the cities we're going to analyze. Run the first code cell below to load some packages and functions that you'll be using in your analysis. Then, complete the second code cell to print out the first trip recorded from each of the cities (the second line of each data file).
# 
# 

# In[5]:


## import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
from pprint import pprint # use to print data structures like dictionaries in
                          # a nicer way than the base print function.


# In[6]:


def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))
    
    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)
        
        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        for row in trip_reader: 
            first_trip = row
            break

        
        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pprint(first_trip)
        
    # output city name and first trip for later testing
    return (city, first_trip)

# list of files for each city
data_files = ['NYC-CitiBike-2016.csv',
              'Chicago-Divvy-2016.csv',
              'Washington-CapitalBikeshare-2016.csv',]

# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip


# If everything has been filled out correctly, you should see below the printout of each city name (which has been parsed from the data file name) that the first trip has been parsed in the form of a dictionary. When you set up a `DictReader` object, the first row of the data file is normally interpreted as column names. Every other row in the data file will use those column names as keys, as a dictionary is generated for each row.
# 
# This will be useful since we can refer to quantities by an easily-understandable label instead of just a numeric index. For example, if we have a trip stored in the variable `row`, then we would rather get the trip duration from `row['duration']` instead of `row[0]`.
# 
# <a id='condensing'></a>
# ### Condensing the Trip Data
# 
# It should also be observable from the above printout that each city provides different information. Even where the information is the same, the column names and formats are sometimes different. To make things as simple as possible when we get to the actual exploration, we should trim and clean the data. Cleaning the data makes sure that the data formats across the cities are consistent, while trimming focuses only on the parts of the data we are most interested in to make the exploration easier to work with.
# 
# You will generate new data files with five values of interest for each trip: trip duration, starting month, starting hour, day of the week, and user type. Each of these may require additional wrangling depending on the city:
# 
# - **Duration**: This has been given to us in seconds (New York, Chicago) or milliseconds (Washington). A more natural unit of analysis will be if all the trip durations are given in terms of minutes.
# - **Month**, **Hour**, **Day of Week**: Ridership volume is likely to change based on the season, time of day, and whether it is a weekday or weekend. Use the start time of the trip to obtain these values. The New York City data includes the seconds in their timestamps, while Washington and Chicago do not. The [`datetime`](https://docs.python.org/3/library/datetime.html) package will be very useful here to make the needed conversions.
# - **User Type**: It is possible that users who are subscribed to a bike-share system will have different patterns of use compared to users who only have temporary passes. Washington divides its users into two types: 'Registered' for users with annual, monthly, and other longer-term subscriptions, and 'Casual', for users with 24-hour, 3-day, and other short-term passes. The New York and Chicago data uses 'Subscriber' and 'Customer' for these groups, respectively. For consistency, you will convert the Washington labels to match the other two.
# 
# 
# **Question 3a**: Complete the helper functions in the code cells below to address each of the cleaning tasks described above.

# In[7]:


def duration_in_mins(datum, city):
   
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.
    
    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds. 
    
    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """
    
    # YOUR CODE HERE
    if city == "Washington":
        duration_string = datum["Duration (ms)"]
        duration = float(duration_string)/60000
    else: 
        duration_string = datum["tripduration"]
        duration = float(duration_string)/60
    return duration


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}


for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001


# In[8]:



    
    # YOUR CODE HERE
    #function to return the name of the weekday based on number: 
def dayNameFromWeekday(weekday):
    if weekday == 0:
        return "Monday"
    if weekday == 1:
        return "Tuesday"
    if weekday == 2:
        return "Wednesday"
    if weekday == 3:
        return "Thursday"
    if weekday == 4:
        return "Friday"
    if weekday == 5:
        return "Saturday"
    if weekday == 6:
        return "Sunday"

def MonthNameFromNumber(month):
    if month == 1:
        return "January"
    if month == 2:
        return "February"
    if month == 3:
        return "March"
    if month == 4:
        return "April"
    if month == 5:
        return "May"
    if month == 6:
        return "June"
    if month == 7:
        return "July"
    if month == 8: 
        return "August"
    if month == 9: 
        return "September"
    if month == 10: 
        return "October"
    if month == 11: 
        return "November"
    if month == 12: 
        return "December"
    
def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.
    
    Remember that NYC includes seconds, while Washington and Chicago do not.
    
    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """
    
    #month, hour, day of the week
    if city == "NYC":
        whentrip_string = (datum["starttime"])
        #splitting out the month and hour into a list to be able to call this into formatted date
        split_list = whentrip_string.split("/")
        month = int(split_list[0])
        day = int(split_list[1])
        #splitting out the next part of the string-next piece is year
        year_list = split_list[2].split(" ")
        year = int(year_list[0])
        #splitting out the next part of the string-next piece is hour
        time_list = year_list[1].split(":")
        hour = int(time_list[0])
        
        
    elif city == "Chicago": 
        whentrip_string = (datum["starttime"])
        #splitting out the month and hour into a list to be able to call this into formatted date
        split_list = whentrip_string.split("/")
        month = int(split_list[0])
        day = int(split_list[1])
        #splitting out the next part of the string-next piece is year
        year_list = split_list[2].split(" ")
        year = int(year_list[0])
        #splitting out the next part of the string-next piece is hour
        time_list = year_list[1].split(":")
        hour = int(time_list[0])
    
    elif city == "Washington":
        whentrip_string = (datum["Start date"])
        #splitting out the month and hour into a list to be able to call this into formatted date
        split_list = whentrip_string.split("/")
        month = int(split_list[0])
        day = int(split_list[1])
        #splitting out the next part of the string-next piece is year
        year_list = split_list[2].split(" ")
        year = int(year_list[0])
        #splitting out the next part of the string-next piece is hour
        time_list = year_list[1].split(":")
        hour = int(time_list[0])
    
    # section to convert the year, month, day, and hour to a day of the week
    dt = datetime(year, month, day, hour)
    weekday = dt.weekday()
    
    #return (month, hour, day_of_week)must add helper functions to convert integers back to strings
    #Reported_month = MonthNameFromNumber(month)
    Reported_month = month
    Reported_hour = hour
    Reported_dayoftheweek = dayNameFromWeekday(weekday)
   
    return (Reported_month, Reported_hour, Reported_dayoftheweek)
    
 

 # Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    #assert time_of_trip(example_trips[city], city) == tests[city]
    time_of_trip(example_trips[city], city) == tests[city]


# In[9]:


def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.
    
    Remember that Washington has different category names compared to Chicago
    and NYC. 
    """
    
    # YOUR CODE HERE
    if city == "Washington":
        user_data = (datum["Member Type"])
        if user_data == "Registered": 
            user_type = "Subscriber"
        else: 
            user_type = "Customer"
        
    else: 
        user_type = (datum["usertype"])
        
    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Subscriber'}

for city in tests:
    assert type_of_user(example_trips[city], city) == tests[city]



# **Question 3b**: Now, use the helper functions you wrote above to create a condensed data file for each city consisting only of the data fields indicated above. In the `/examples/` folder, you will see an example datafile from the [Bay Area Bike Share](http://www.bayareabikeshare.com/open-data) before and after conversion. Make sure that your output is formatted to be consistent with the example file.

# In[12]:


def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.
    
    HINT: See the cell below to see how the arguments are structured!
    """
    
    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()
        
        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)
       
            
        
        
        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            current_trip = row
            ret = time_of_trip(current_trip,city)
            new_point = {'duration': (duration_in_mins(current_trip,city)), 'month': ret[0],
                        'hour': ret[1], 'day_of_week': ret[2], 'user_type': (type_of_user(current_trip,city))}
            

            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            
            trip_writer.writerow(new_point)
            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
         
        

   
            
            


# In[13]:


# Run this cell to check your work
city_info = {'Washington': {'in_file': 'Washington-CapitalBikeshare-2016.csv',
                            'out_file': 'Washington-2016-Summary.csv'},
             'Chicago': {'in_file': 'Chicago-Divvy-2016.csv',
                         'out_file': 'Chicago-2016-Summary.csv'},
             'NYC': {'in_file': 'NYC-CitiBike-2016.csv',
                     'out_file': 'NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])


# > **Tip**: If you save a jupyter Notebook, the output from running code blocks will also be saved. However, the state of your workspace will be reset once a new session is started. Make sure that you run all of the necessary code blocks from your previous session to reestablish variables and functions before picking up where you last left off.
# 
# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# Now that you have the data collected and wrangled, you're ready to start exploring the data. In this section you will write some code to compute descriptive statistics from the data. You will also be introduced to the `matplotlib` library to create some basic histograms of the data.
# 
# <a id='statistics'></a>
# ### Statistics
# 
# First, let's compute some basic counts. The first cell below contains a function that uses the csv module to iterate through a provided data file, returning the number of trips made by subscribers and customers. Modify the cells to answer the question below.
# 
# **Question 4a**: Which city has the highest number of trips? Which city has the highest proportion of trips made by subscribers? Which city has the highest proportion of trips made by short-term customers?
# 
# **Answer**: New York City had the greatest number of trips. New York had the highest proportion of trips made by subscribers. Washington had the highest proportion of trips made by short term customers. 

# In[16]:


def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_subscribers = 0
        n_customers = 0
        
        # tally up ride types
        for row in reader:
            if row['user_type'] == 'Subscriber':
                n_subscribers += 1
            else:
                n_customers += 1
        
        # compute total number of rides
        n_total = n_subscribers + n_customers
        
        # return tallies as a tuple
        return(n_subscribers, n_customers, n_total)


# In[18]:


## Modify this and the previous cell to answer Question 4a. Remember to run ##
## the function on the cleaned data files you created from Question 3.      ##


data_file1 = 'Washington-2016-Summary.csv'
data_file2 = 'Chicago-2016-Summary.csv'
data_file3 = 'NYC-2016-Summary.csv'

print(number_of_trips(data_file1))
print(number_of_trips(data_file2))
print(number_of_trips(data_file3))




# > **Tip**: In order to add additional cells to a notebook, you can use the "Insert Cell Above" and "Insert Cell Below" options from the menu bar above. There is also an icon in the toolbar for adding new cells, with additional icons for moving the cells up and down the document. By default, new cells are of the code type; you can also specify the cell type (e.g. Code or Markdown) of selected cells from the Cell menu or the dropdown in the toolbar.
# 
# Now, you will write your own code to continue investigating properties of the data.
# 
# **Question 4b**: Bike-share systems are designed for riders to take short trips. Most of the time, users are allowed to take trips of 30 minutes or less with no additional charges, with overage charges made for trips of longer than that duration. What is the average trip length for each city? What proportion of rides made in each city are longer than 30 minutes?
# 
# **Answer**: The average trip length for Washington: 19 min, proportion longer than 30 min: 11% 
# The average trip length for Chiago: The average trip length for Chicago: 17 min, proportion longer than 30 min: 8.3%
# The average trip for New York: 16 min, proportion longer than 30 min: 7.3%

# In[19]:


## Use this and additional cells to answer Question 4b.                 ##
##                                                                      ##
## HINT: The csv module reads in all of the data as strings, including  ##
## numeric values. You will need a function to convert the strings      ##
## into an appropriate numeric type before you aggregate data.          ##
## TIP: For the Bay Area example, the average trip length is 14 minutes ##
## and 3.5% of trips are longer than 30 minutes.                        ##



# In[20]:


def duration_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_trips_lessthan30 = 0
        n_tripsgreaterthan30 = 0
        duration_sum = 0
        
        # tally up total duration (to be used in average calculation) and tally up trips less than 30 min and 
        #greater than 30 min
        for row in reader:
            converted_duration = float(row['duration'])
            duration_sum = duration_sum + converted_duration
            if converted_duration <=  30:
                n_trips_lessthan30 += 1
            else:
                n_tripsgreaterthan30 += 1
        
        # compute average trip duration
        total_trips = n_trips_lessthan30 + n_tripsgreaterthan30
        average_duration = duration_sum / total_trips
        
        # return tallies and average as a tuple
        return(n_trips_lessthan30, n_tripsgreaterthan30, average_duration)
    

data_file1 = 'Washington-2016-Summary.csv'
data_file2 = 'Chicago-2016-Summary.csv'
data_file3 = 'NYC-2016-Summary.csv'

print(duration_of_trips(data_file1))
print(duration_of_trips(data_file2))
print(duration_of_trips(data_file3))
    


# **Question 4c**: Dig deeper into the question of trip duration based on ridership. Choose one city. Within that city, which type of user takes longer rides on average: Subscribers or Customers?
# 
# **Answer**: In Washington the average subscriber trip is 12.5 minutes and the average customer trip is longer at 41.7 minutes. 

# In[22]:


## Use this and additional cells to answer Question 4c. If you have    ##
## not done so yet, consider revising some of your previous code to    ##
## make use of functions for reusability.                              ##
##                                                                     ##
## TIP: For the Bay Area example data, you should find the average     ##
## Subscriber trip duration to be 9.5 minutes and the average Customer ##
## trip duration to be 54.6 minutes. Do the other cities have this     ##
## level of difference?                                                ##

def avg_durationbytype(filename):
    """
    This function reads in a file with trip data and reports the average duration of
    the trips made by subscribers and customers. 
    """
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        
        # initialize count variables
        n_subscribers = 0
        n_customers = 0
        count = 0
        total_subscriberduration = 0
        total_customerduration = 0
        
        # tally up ride types, sum of duration of trips to be used in the calculation 
        #of average
        for row in reader:
            count += 1
            #print ("str duration: ", row["duration"])
            converted_duration = float(row['duration'])
            #print ("converted_duration: ", converted_duration)

            if row['user_type'] == 'Subscriber':
                n_subscribers += 1
                total_subscriberduration = total_subscriberduration + converted_duration
                #print ("total_subscriberduration: ", total_subscriberduration)
            else:
                n_customers += 1
                total_customerduration = total_customerduration + converted_duration
                #print ("total_customerduration: ", total_customerduration)

        # TODO check for divide-by-zero
        # compute the average duration of rides
        #for subscribers: 
        avg_durationsubscribers = total_subscriberduration / n_subscribers
        #print ("avg_durationsubscribers: {0}, {1}, {2}".format(avg_durationsubscribers, 
        #total_subscriberduration, n_subscribers))
        
        avg_durationcustomers = total_customerduration / n_customers
        #print ("avg_durationcustomers: ", total_customerduration)
        
        return (n_subscribers, avg_durationsubscribers, n_customers, avg_durationcustomers)
    

data_file1 = 'Washington-2016-Summary.csv'
data_file2 = 'Chicago-2016-Summary.csv'
data_file3 = 'NYC-2016-Summary.csv'

print(avg_durationbytype(data_file1))
print(avg_durationbytype(data_file2))
print(avg_durationbytype(data_file3))

    
    


# <a id='visualizations'></a>
# ### Visualizations
# 
# The last set of values that you computed should have pulled up an interesting result. While the mean trip time for Subscribers is well under 30 minutes, the mean trip time for Customers is actually _above_ 30 minutes! It will be interesting for us to look at how the trip times are distributed. In order to do this, a new library will be introduced here, `matplotlib`. Run the cell below to load the library and to generate an example plot.

# In[23]:


# load library
import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().magic('matplotlib inline')

# example histogram, data taken from bay area sample
data = [ 7.65,  8.92,  7.42,  5.50, 16.17,  4.20,  8.98,  9.62, 11.48, 14.33,
        19.02, 21.53,  3.90,  7.97,  2.62,  2.67,  3.08, 14.40, 12.90,  7.83,
        25.12,  8.30,  4.93, 12.43, 10.60,  6.17, 10.88,  4.78, 15.15,  3.53,
         9.43, 13.32, 11.72,  9.85,  5.22, 15.10,  3.95,  3.17,  8.78,  1.88,
         4.55, 12.68, 12.38,  9.78,  7.63,  6.45, 17.38, 11.90, 11.52,  8.63,]
plt.hist(data)
plt.title('Distribution of Trip Durations')
plt.xlabel('Duration (m)')
plt.show()


# In the above cell, we collected fifty trip times in a list, and passed this list as the first argument to the `.hist()` function. This function performs the computations and creates plotting objects for generating a histogram, but the plot is actually not rendered until the `.show()` function is executed. The `.title()` and `.xlabel()` functions provide some labeling for plot context.
# 
# You will now use these functions to create a histogram of the trip times for the city you selected in question 4c. Don't separate the Subscribers and Customers for now: just collect all of the trip times and plot them.

# In[25]:


## Use this and additional cells to collect all of the trip times as a list ##
## and then use pyplot functions to generate a histogram of trip times.     ##
# load library
#import matplotlib.pyplot as plt

# this is a 'magic word' that allows for plots to be displayed
# inline with the notebook. If you want to know more, see:
# http://ipython.readthedocs.io/en/stable/interactive/magics.html
#%matplotlib inline 

# function to create a list based on reading a dictionary "Washington"

def duration_plotdata(filename):
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        list = []
        for row in reader: 
            converted_duration = float(row['duration'])
            list.append(converted_duration)
        return list


data_to_plot = duration_plotdata('Washington-2016-Summary.csv')
plt.hist(data_to_plot)
plt.title('Distribution of Trip Durations for Washington')
plt.xlabel('Duration (m)')
plt.show()

   
            


# If you followed the use of the `.hist()` and `.show()` functions exactly like in the example, you're probably looking at a plot that's completely unexpected. The plot consists of one extremely tall bar on the left, maybe a very short second bar, and a whole lot of empty space in the center and right. Take a look at the duration values on the x-axis. This suggests that there are some highly infrequent outliers in the data. Instead of reprocessing the data, you will use additional parameters with the `.hist()` function to limit the range of data that is plotted. Documentation for the function can be found [[here]](https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist).
# 
# **Question 5**: Use the parameters of the `.hist()` function to plot the distribution of trip times for the Subscribers in your selected city. Do the same thing for only the Customers. Add limits to the plots so that only trips of duration less than 75 minutes are plotted. As a bonus, set the plots up so that bars are in five-minute wide intervals. For each group, where is the peak of each distribution? How would you describe the shape of each distribution?
# 
# **Answer**: For subscribers, the peak of the distribution is in the 5-10 min range. For customers, the peak of the distribution is in the 15-20 min range. The shape of the customer distribution is skewed to the left, while for the customers, the distribution is also skewed to the left but not as much as the substribers. 

# In[27]:


## Use this and additional cells to answer Question 5. ##
## First create a list of only the subscriber data
## Then create a list of only the customer data
## Create if then so that only items with a duration of less than 75 minutes are added to the list

def plot_function(filename):
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        subscriber_list = []
        customer_list = []
        for row in reader: 
            converted_duration = float(row['duration'])
            if converted_duration < 75: 
            #create conditional statement about which list the duration should go into
                if row['user_type'] == 'Subscriber':
                    subscriber_list.append(converted_duration)
            
                else: 
                    customer_list.append(converted_duration)
            
               
            
        return subscriber_list, customer_list
    #subscriber list is [0] from the function returned list
    #customer list is [1] from the function returned list
        
        

#data_file1 = './data/Washington-2016-Summary.csv'
#prints the first three from each lists (2 lists are returned from the function)
#print (plot_function(data_file1))
#prints the first list returned from the function
#print (plot_function(data_file1)[1])

#Plot for subscribers: 
data_to_plot1 = (plot_function('Washington-2016-Summary.csv')[0])
plt.hist(data_to_plot1, bins = 15)
plt.title('Distribution of Trip Durations for Washington Subscribers')
plt.xlabel('Duration (m)')
plt.ylabel('Number of Riders')
plt.axis([0,75,0,18000])
binmids = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5, 62.5, 67.5, 72.5]
plt.xticks(binmids)

plt.grid(True)
plt.show()


#Plot for customers: 
data_to_plot1 = (plot_function('Washington-2016-Summary.csv')[1])
plt.hist(data_to_plot1, bins = 15)
plt.title('Distribution of Trip Durations for Washington Customers')
plt.xlabel('Duration (m)')
plt.ylabel('Number of Riders')
plt.axis([0,75,0,2500])
binmids = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5, 62.5, 67.5, 72.5]
plt.xticks(binmids)

plt.grid(True)
plt.show()



   



# <a id='eda_continued'></a>
# ## Performing Your Own Analysis
# 
# So far, you've performed an initial exploration into the data available. You have compared the relative volume of trips made between three U.S. cities and the ratio of trips made by Subscribers and Customers. For one of these cities, you have investigated differences between Subscribers and Customers in terms of how long a typical trip lasts. Now it is your turn to continue the exploration in a direction that you choose. Here are a few suggestions for questions to explore:
# 
# - How does ridership differ by month or season? Which month / season has the highest ridership? Does the ratio of Subscriber trips to Customer trips change depending on the month or season?
# - Is the pattern of ridership different on the weekends versus weekdays? On what days are Subscribers most likely to use the system? What about Customers? Does the average duration of rides change depending on the day of the week?
# - During what time of day is the system used the most? Is there a difference in usage patterns for Subscribers and Customers?
# 
# If any of the questions you posed in your answer to question 1 align with the bullet points above, this is a good opportunity to investigate one of them. As part of your investigation, you will need to create a visualization. If you want to create something other than a histogram, then you might want to consult the [Pyplot documentation](https://matplotlib.org/devdocs/api/pyplot_summary.html). In particular, if you are plotting values across a categorical variable (e.g. city, user type), a bar chart will be useful. The [documentation page for `.bar()`](https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar) includes links at the bottom of the page with examples for you to build off of for your own use.
# 
# **Question 6**: Continue the investigation by exploring another question that could be answered by the data available. Document the question you want to explore below. Your investigation should involve at least two variables and should compare at least two groups. You should also use at least one visualization as part of your explorations.
# 
# **Answer**: My question relates to ridership based on the month? Is this the same for each city?Also, is this the same for subscribers and customers? 
# Answer based on the graphs below: Using Washington as an example and based on the graphs below, it appears that ridership for subsribers remains fairly consistent throughout the year, with a drop in the winter months Dec, Jan, and Feb. For customers, there is a visible increase in ridership during the summer months, particularly July when compared to the rest of the year. 

# In[29]:


## Use this and additional cells to continue to explore the dataset. ##
## Once you have performed your exploration, document your findings  ##
## in the Markdown cell above.                                       ##

## Use this and additional cells to answer Question 5. ##
## First create a list of only the subscriber data
## Then create a list of only the customer data
## Create if then so that only items with a duration of less than 75 minutes are added to the list

def plot_function(filename):
    with open(filename, 'r') as f_in:
        # set up csv reader object
        reader = csv.DictReader(f_in)
        subscriber_list_month = []
        customer_list_month = []
        for row in reader: 
            month_of_trip = int(row['month']) 
            #create conditional statement about which list the month should go into(subscriber or customer)
            if row['user_type'] == 'Subscriber':
                subscriber_list_month.append(month_of_trip)
            else: 
                customer_list_month.append(month_of_trip)
        return sorted(subscriber_list_month), sorted(customer_list_month)
            


#Plot for subscribers in Washington: 
data_to_plot1 = (plot_function('Washington-2016-Summary.csv')[0])
plt.figure(figsize=(5,5))
plt.title('Distribution of Trip Months for Washington Subscribers')
plt.xlabel('Month (m)')
plt.ylabel('Number of Riders')
plt.axis([-1,12,0,8000]) 
bin_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
possible_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
fin = [ possible_months.index(i) for i in data_to_plot1]
plt.hist(fin, bins=range(13), align="left")
plt.xticks(range(12), bin_labels)
plt.grid(True)
plt.show()

#Plot for customers in Washington: 
data_to_plot2 = (plot_function('Washington-2016-Summary.csv')[1])
plt.figure(figsize=(5,5))
plt.title('Distribution of Trip Months for Washington Customers')
plt.xlabel('Month (m)')
plt.ylabel('Number of Riders')
plt.axis([-1,12,0,2500]) 
bin_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
possible_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
fin = [ possible_months.index(i) for i in data_to_plot2]
plt.hist(fin, bins=range(13), align="left")
plt.xticks(range(12), bin_labels)
plt.grid(True)
plt.show()




            


# # <a id='conclusions'></a>
# ## Conclusions
# 
# Congratulations on completing the project! This is only a sampling of the data analysis process: from generating questions, wrangling the data, and to exploring the data. Normally, at this point in the data analysis process, you might want to draw conclusions about the data by performing a statistical test or fitting the data to a model for making predictions. There are also a lot of potential analyses that could be performed on the data which are not possible with only the data provided. For example, detailed location data has not been investigated. Where are the most commonly used docks? What are the most common routes? As another example, weather has potential to have a large impact on daily ridership. How much is ridership impacted when there is rain or snow? Are subscribers or customers affected more by changes in weather?
# 
# **Question 7**: Putting the bike share data aside, think of a topic or field of interest where you would like to be able to apply the techniques of data science. What would you like to be able to learn from your chosen subject?
# 
# **Answer**: I am very interested in the field of public health. So for example, vaccination rates and instances of certain diseases. 
# 
# > **Tip**: If we want to share the results of our analysis with others, we aren't limited to giving them a copy of the jupyter Notebook (.ipynb) file. We can also export the Notebook output in a form that can be opened even for those without Python installed. From the **File** menu in the upper left, go to the **Download as** submenu. You can then choose a different format that can be viewed more generally, such as HTML (.html) or
# PDF (.pdf). You may need additional packages or software to perform these exports.
