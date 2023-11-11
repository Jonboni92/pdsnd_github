import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data.")

    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input('Enter the city (Chicago, New York City, Washington):\n').lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from Chicago, New York City, or Washington.")

    # Get user input for month (all, january, february, ..., june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Enter the month (all, January, February, ..., June):\n').lower()
        if month in months:
            break
        else:
            print("Invalid month. Please choose from all, January, February, March, April, May, June.")

    # Get user input for the day of the week (all, Monday, Tuesday, ..., Sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Enter the day of the week (all, Monday, Tuesday, ..., Sunday):\n').lower()
        if day in days:
            break
        else:
            print("Invalid day. Please choose from all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the data for the selected city
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    # Filter the data based on user input for month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    # Filter the data based on user input for day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('Most common month: {}'.format(df['month'].mode()[0]))

    # Display the most common day of the week
    print('Most common day of the week: {}'.format(df['day_of_week'].mode()[0]))

    # Display the most common start hour
    print('Most common start hour: {}'.format(df['start_hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('Most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    df['combination'] = "Starts at: " + df['Start Station'] + ",  finishes at: " + df['End Station']
    print('The most common start-end combination: {}'.format(df['combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # Display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    if 'Gender' in df:
        # Display counts of gender
        print(df['Gender'].value_counts().to_frame())

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: ', int(df['Birth Year'].min()))
        print('Most recent year of birth: ', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mode()[0]))
    else:
        print('This city has no user data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def raw_data(df):
    """Prompts user if they want to see 5 lines of raw data."""
    print('\nRaw data available. \n')
    
    i = 0
    user_input = input('Do you want to display 5 lines of raw data? Type yes to proceed. Else type no to terminate this process:\n').lower()
    if user_input not in ['yes', 'no']:
        print('Invalid answer. Type yes or no.')
        user_input = input('Do you want to display 5 lines of raw data? Type yes to proceed. Else, type no to terminate this process:\n').lower()
    elif user_input != 'yes':
        print('Terminating process...')
        
    else:
        while i + 5 < df.shape[0]:
            print(df.iloc[i:i + 5])
            i += 5
            user_input = input('Do you want to display 5 more lines of raw data? Type yes to proceed. Else, type no to terminate this process:\n').lower()
            if user_input != 'yes':
                print('Terminating process...')
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no:\n')
        if restart.lower() != 'yes':
            print('Ending program... Goodbye.')
            break

if __name__ == "__main__":
    main()
