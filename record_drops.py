import os
from datetime import datetime
import csv

# Since time and day are used throughout the whole program they are
# declared as global variables to avoid unnecessary definitions of the variables
time = datetime.now().time()
day = datetime.now().weekday()


def check_day():
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
            if row['Day'] == get_day(day):
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
    with open('faults.csv', 'a', newline='') as file:
        headings = ['Time', 'Day']
        write = csv.DictWriter(file, fieldnames=headings)
        write.writerow({'Time': time, 'Day': get_day(day)})
    file.close()
    ping()


def write_to_csv():
    """
        Writes the time of connection drops and the day it occurs
        to a csv.
    """
    with open('faults.csv', 'w', newline='') as file:
        headings = ['Time', 'Day']
        write = csv.DictWriter(file, fieldnames=headings)
        write.writeheader()
        write.writerow({'Time': time, 'Day': get_day(day)})
    file.close()
    ping()


def ping():
    """
        Pings the Google DNS server to check whether the connection is on or off
    """
    check = os.system('ping 8.8.8.8')
    if check == 0:
        check_day()
    else:
        check_day()


def main():
    initiate = 0
    if initiate == 0:
        # Is initiated each time the program starts
        # since the program shouldn't stop, this statement will only run once
        with open('faults.csv', 'w', newline='') as file:
            headings = ['Time', 'Day']
            write = csv.DictWriter(file, fieldnames=headings)
            write.writeheader()
            write.writerow({'Time': None, 'Day': None})     # Initiates csv with None values
        ping()
        initiate += 1

    # Shouldn't reach this point, if it does the program will finish
    return False


if __name__ == "__main__":
    main()
