
import time
import pandas as pd
import numpy as np
import sys
import datetime as dt
from ast import Break

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters( ):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # specify global variables :
    global city, month, day, month_name
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city :
    cities = list(CITY_DATA)
    city = input('Which city do you want to explore ?\n{}'.format(cities)).lower()
    
    while not city in cities:
        print('/!\ {} : is not a correct city. Please check your input'.format(city))
        city = input('Which city do you want to explore ?').lower()
    
    print('----> {} : is selected for exploration'.format(city))
    
    
    # get user input for month :
    month = input('Which month do you want to explore ? \n(all, january, february, ... , december)').title()
    month_name = month
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December']
        while not month in months:
            print('/!\ {} : is not a correct month. Please check your input'.format(month))
            month = input('Which month do you want to explore ?').title()
        month = months.index(month.title())+1
        print('----> {} : is selected for exploration'.format(months[month-1]))
    
    else:
        print('----> All months are selected for exploration')       
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day do you want to explore ? \n(all, monday, tuesday, ... sunday)').title()
    
    if day != 'All':
        # check if days is correct usint a list of corrrect days :
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        while not day in days:
            print('/!\ {} : is not a correct day. Please check your input'.format(day))
            day = input('Which day do you want to explore ?').title()
        print('----> {} : is selected for exploration'.format(day))
    else :
        print('----> All days are selected for exploration')
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # specify global variables :
    global df
    
    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city])
    except KeyError:
        print('Datasource (file : {}) doesn\'t exist.\n End of execution.'.format(city))
        sys.exit()
    
    # convert the Start Time column to datetime, if not possible => NaT
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    #remove NaT from dataframe to secure we have only datetime values :
    df = df.dropna()
     # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]
        
    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('Scope = City: {}, month(s): {}, day(s): {}'.format(city, month_name,day))
    start_time = time.time()
  
    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = np.count_nonzero(df['month'] == popular_month)
    popular_month_Percent = round(popular_month_count/np.count_nonzero(df['month'])*100, 1)
    print('Most Frequent Month: {} (count= {}, %= {}) '.format( popular_month, popular_month_count, popular_month_Percent))

    # display the most common week
    # extract week from the Start Time column to create an week column
    df['week'] = df['Start Time'].dt.isocalendar().week
    # find the most common week
    popular_week = df['week'].mode()[0]
    popular_week_count = np.count_nonzero(df['week'] == popular_week)
    popular_week_Percent = round(popular_week_count/np.count_nonzero(df['week'])*100, 1)
    print('Most Frequent Week: {} (count= {}, %= {}) '.format( popular_week, popular_week_count, popular_week_Percent))

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    popular_DoW_count = np.count_nonzero(df['day_of_week'] == popular_day_of_week)
    popular_DoW_Percent = round(popular_DoW_count/np.count_nonzero(df['day_of_week'])*100, 1)
    print('Most Frequent Day in Week: {} (count= {}, %= {}) '.format( popular_day_of_week, popular_DoW_count, popular_DoW_Percent))
    
    
    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = np.count_nonzero(df['hour'] == popular_hour)
    popular_hour_Percent = round(popular_hour_count/np.count_nonzero(df['hour'])*100, 1)
    print('Most Frequent Start Hour: {} (count= {}, %= {}) '.format( popular_hour, popular_hour_count, popular_hour_Percent))
    
    
    print("\nThis took %s seconds." % duration_up_now(start_time))
    print('-'*40)


def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('Scope = City: {}, month(s): {}, day(s): {}'.format(city, month_name,day))
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = np.count_nonzero(df['Start Station'] == popular_start_station)
    popular_start_station_Percent = round(popular_start_station_count/np.count_nonzero(df['Start Station'])*100, 1)
    print('Most Frequent Start Station: {} (count= {}, %= {}) '.format( popular_start_station, popular_start_station_count, popular_start_station_Percent))
   

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = np.count_nonzero(df['End Station'] == popular_end_station)
    popular_end_station_Percent = round(popular_end_station_count/np.count_nonzero(df['End Station'])*100, 1)
    print('Most Frequent End Station: {} (count= {}, %= {}) '.format( popular_end_station, popular_end_station_count, popular_end_station_Percent))

    # display most frequent combination of start station and end station trip
    # extract combination Start / End Station in a new column.
    df['Trip'] = "From [" + df['Start Station'] + "] To [" + df['End Station'] + "]"
    popular_trip = df['Trip'].mode()[0]
    popular_trip_count = np.count_nonzero(df['Trip'] == popular_trip)
    popular_trip_Percent = round(popular_trip_count/np.count_nonzero(df['Trip'])*100, 1)
    print('Most Frequent Trip: {} (count= {}, %= {}) '.format( popular_trip, popular_trip_count, popular_trip_Percent))
    

    print("\nThis took %s seconds." % (duration_up_now(start_time)))
    print('-'*40)

def duration_up_now(start_time):
    '''
        extract method used to create the  function 
        (refactoring)
    '''
    return time.time() - start_time


def trip_duration_stats(df):
    
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('Scope = City: {}, month(s): {}, day(s): {}'.format(city, month_name,day))
    start_time = time.time()

    # convert the End Time column to datetime, if not possible => NaT
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')
    #remove NaT from dataframe to secure we have only datetime values :
    df = df.dropna()
    # calculate duration and add it as new column :
    df['Total_Travel_Time'] = df['End Time'] - df['Start Time']
    
    # display total travel time info :
    Max_Travel_Time = df['Total_Travel_Time'].max()
    Min_Travel_Time = df['Total_Travel_Time'].min()
    #print(df['Total_Travel_Time'].value_counts())
    print('Max travel time is : {}'.format(Max_Travel_Time))
    print('Min travel time is : {}'.format(Min_Travel_Time))

    # display mean travel time
    Mean_Travel_Time = df['Total_Travel_Time'].mean()
    print('Mean travel time is : {}'.format(Mean_Travel_Time))

    print("\nThis took %s seconds." % duration_up_now(start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
 
    print('\nCalculating User Stats...\n')
    print('Scope = City: {}, month(s): {}, day(s): {}'.format(city, month_name,day))
    start_time = time.time()

    # Display counts of user types
    try:
        # fill in empty value with 'empty':
        df['User Type'] = df['User Type'].fillna('empty')
   
        User_Type_Count = df['User Type'].value_counts()
        User_Type_Percent = df['User Type'].value_counts(normalize=True).mul(100).round(1)
        UserTypesDisplay = pd.DataFrame({'Units' : User_Type_Count, '%' : User_Type_Percent})
        print('User types are dispayed like this:\n{}'.format(UserTypesDisplay))
    except KeyError:
        print ('\n[User Type] doesn\'t exists for this scope of data. Display is not possible')
    
    # Display counts of gender
    try:
        # fill in empty value with 'empty':
        df['Gender'] = df['Gender'].fillna('empty')
        Gender_Count = df['Gender'].value_counts()
        Gender_Percent = df['Gender'].value_counts(normalize=True).mul(100).round(1)
        GenderDisplay = pd.DataFrame({'Units' : Gender_Count, '%' : Gender_Percent})
        print('\nGender are dispayed like this:\n{}'.format(GenderDisplay))
    except KeyError:
        print ('\n[Gender] doesn\'t exists for this scope of data. Display is not possible')
     
   

    # Display earliest, most recent, and most common year of birth
    # fill in empty value with '0':
    try:
        df['Birth Year'] = df['Birth Year'].fillna(0)
    
        Earliest_Birth_Year = df['Birth Year'].loc[df['Birth Year'] > 0].min()
        Most_Recent_Birth_Year = df['Birth Year'].loc[df['Birth Year'] > 0].max()
        Most_Common_Birth_Year = df['Birth Year'].loc[df['Birth Year'] > 0].mode()[0]
        print('\nEarliest Year of birth is: {}'.format(int(Earliest_Birth_Year)))
        print('Most recent Year of birth is: {}'.format(int(Most_Recent_Birth_Year)))
        print('Most common Year of birth is: {}'.format(int(Most_Common_Birth_Year)))
    except KeyError:
        print ('\n[Birth Year] doesn\'t exists for this scope of data. Display is not possible')

            
    print("\nThis took %s seconds." % duration_up_now(start_time))
    print('-'*40)

def see_raw_data(df):

    """Displays Raw data, if user wants it."""
    print('Scope = City: {}, month(s): {}, day(s): {}'.format(city, month_name,day))
    answer, cycle, line_start = 'Y', '',0
    remaining_lines = len(df) - line_start
    while True:
        print('Remaining lines:{}'.format(remaining_lines))
        if remaining_lines > 0 and answer.upper() == 'Y':
            Raw_Data_To_See = df[line_start:line_start + 5]
            print(Raw_Data_To_See)
            line_start = line_start + 5
            remaining_lines = len(df) - line_start
            cycle = 'more '
            answer = input('Do you want to see 5 {}lines of raw data (Y or N) ? '.format(cycle)) 
        else:
            print('End of analysis')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('Scope = City: {}, month(s): {}, day(s): {}'.format(city, month_name,day))
        if len(df) >0:  # if data in the scope
            print('dataframe size : {} lines'.format(len(df)))
            if input('Do you want to see Time statistics ? (Y or N)').upper()=='Y':
                time_stats(df)
            if input('Do you want to see Station statistics ? (Y or N)').upper()=='Y':
                station_stats(df)
            if input('Do you want to see Trip statistics ? (Y or N)').upper()=='Y':
                trip_duration_stats(df)
            if input('Do you want to see User statistics ? (Y or N)').upper()=='Y':
                user_stats(df)
            if input('Do you want to see 5 lines of Raw Data ? (Y or N)').upper()=='Y':
                see_raw_data(df)
        else: # in case of no data in the scope
            print('no data in selected scope')

        restart = input('\nWould you like to restart? (Y or N).\n')
        if restart.upper() != 'Y':
            break


if __name__ == "__main__":
	main()
