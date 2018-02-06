import os
from datetime import datetime, date
import time
import csv

# Since time and day are used throughout the whole program they are
# declared as global variables to avoid unnecessary redefinitions of the variables
rec_time = datetime.now().time()
rec_day = datetime.now().weekday()


def record_duration():
    """
        Records from when connection drop occurs to the time it is restored,
        returns the time between drop and restoration
    """
    start_time = time.time()
    ping()
    while ping() != 0:
        ping()

    return time.time() - start_time


def check_day_value():
    """
        Reads the data in the 'Day' column from faults.csv,
        if the days are the same it will tell update_csv() to append data,
        else it will tell write_to_csv() to overwrite data.
        This is used to ensure the file is updated with only the current days faults.
    """
    with open('faults.csv', 'r') as file:
        read = csv.DictReader(file)
        for row in read:
            print(row['Day'])
            if row['Day'] == get_day(rec_day):
                print('appended')
                update_csv()
            else:
                print('rewritten')
                write_to_csv()


def get_day(d):
    """
        Returns the value for the weekday:
            0: Monday, 1: Tuesday, 2: Wednesday, 3: Thursday,
            4: Friday, 5: Saturday, 6: Sunday
    """
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day = day_list[d]
    return current_day


def update_csv():
    """
        Appends data to faults.csv
    """
    duration =  record_duration()
    with open('faults.csv', 'a', newline='') as file:
        headings = ['Time', 'Day', 'Duration']
        write = csv.DictWriter(file, fieldnames=headings)
        write.writerow({'Time': rec_time, 'Day': get_day(rec_day), 'Duration': duration})
    file.close()
    connection_check()


def write_to_csv():
    """
        Writes the time of connection drops and the day it occurs
        to a csv.
    """
    duration = record_duration()
    with open('faults.csv', 'w', newline='') as file:
        headings = ['Time', 'Day', 'Duration']
        write = csv.DictWriter(file, fieldnames=headings)
        write.writeheader()
        write.writerow({'Time': rec_time, 'Day': get_day(rec_day), 'Duration': duration})
    file.close()
    connection_check()


def ping():
    """
        Pings the Google DNS server to check whether the connection is on or off
    """
    conn = os.system('ping 8.8.8.8')
    return conn


def connection_check():
    while ping() == 0:
        ping()
    else:
        check_day_value()


def main():
    with open('faults.csv', 'w', newline='') as file:
        headings = ['Time', 'Day', 'Duration']
        write = csv.DictWriter(file, fieldnames=headings)
        write.writeheader()
        write.writerow({'Time': None, 'Day': None, 'Duration': None})  # Initiates csv with None values

    connection_check()


if __name__ == "__main__":
    main()
