import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Which city would you like to analyze ? choose from (chicago - new york city - washington):  ')).lower()
            if city=='chicago' or city=='new york city'or city=='washington':
                break
            else:
                print('Enter the correct name for one of the cities from the choices')
        except:
            print('that is not a valid entry!')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Which month would you like to analyze from january to june ?Type all if you do not want to specify a certain month:  ')).lower()
            if month in ["january","february","march","april","may","june"] or month=='all':
                break
            else:
                print('Enter a correct month or type all for no specific month')
        except:
            print('that is not a valid entry!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Which day would you like to analyze ? Type all if you do not want to specify a certain day:  ')).lower()
            if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
                break
            else:
                print('Enter a correct day or type all for no specific day')
        except:
            print('that is not a valid entry!')

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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    """
    I didn't notice the Trip duration column at first so i added this part of code
    but once i noticed it i changed it to what it should have been
    """
    #df['T1'] = (df['End Time'] - df['Start Time']).dt.seconds

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Common Month:', months[int(df['month'].mode()[0] - 1)].title() )

    # display the most common day of week
    print('Most Common Day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most Common Starting hour:', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Common Starting station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Common Ending station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Start End']=df['Start Station']+' to '+df['End Station']
    print('Most Common Starting and Ending stations combination:', df['Start End'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    print("Total travel time is: {} Days, {} Hours, {} Minutes and {} Seconds".format(df['Trip Duration'].sum()//86400,(df['Trip Duration'].sum()%86400)//3600,((df['Trip Duration'].sum()%86400)%3600//60),(((df['Trip Duration'].sum()%86400)%3600)%60)))
    #print(df['T1'].sum())

    # display mean travel time

    print("Average travel time is: {} Minutes and {} Seconds".format(int(((df['Trip Duration'].mean()%86400)%3600//60)),int((((df['Trip Duration'].mean()%86400)%3600)%60))))
    # print(df['T1'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('-' * 40)
    # Display counts of user types
    print(df['User Type'].value_counts())
    print('-' * 40)
    # Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
        print('-' * 40)
        # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("Earliest birthdate: {}\nMost recent birthdate: {}\nMost common birthdate: {}".format(int(df['Birth Year'].min()),int(df['Birth Year'].max()),int(df['Birth Year'].mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_rows(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data =="yes":
      print(df.iloc[start_loc:start_loc+5])
      start_loc += 5
      view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_rows(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
