import requests
import datetime


def saturday_entry(name):
    return "candles" == name  # Checks whether the input is Candle lighting


def end_of_saturday(name):
    return "havdalah" == name  # Checks whether the input is Havdalah


def saturday_time(name):
    return name.split(' ')[-1]  # Divides the data to extract the time (time is the last organ)


def date_str_to_time(date_str):  # Converts from string to time object
    #  The date is recorded until the letter T
    date_time = datetime.datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
    return date_time


def get_coordinates_and_validate():
    while True:
        try:
            location = int(input("Enter your location (Ashdod is 295629):   "))
            # Cases of exception
        except ValueError:
            print("The coordinates must be an integer/number ,try new input")
        else:
            return location


def get_json_from_api(location):
    calendar = requests.get(f"https://www.hebcal.com/shabbat/?cfg=json&geonameid={location}&m=50")
    return calendar.json()


def get_times_from_json(json_items):
    # Creates a empty dictionary containing all the saturday data
    times = dict()
    for saturday in json_items:

        date = date_str_to_time(saturday["date"])

        if saturday_entry(saturday["category"]):
            # get saturday entry information
            # fills the dictionary
            times['entry'] = saturday_time(saturday['title'])
            times['entry_date'] = date

        elif end_of_saturday(saturday["category"]):
            # get saturday end information
            # fills the dictionary
            times['end'] = saturday_time(saturday['title'])
            times['end_date'] = date
            break  # Coming out of the loop when we got to Saturday of the week
    return times


def print_times(times):
    # Prints to the screen entry/end times of saturday
    print(f"The entry of saturday ({times['entry_date'].date()}) is: {times['entry']}")
    print(f"The end of saturday ({times['end_date'].date()}) is: {times['end']}")


while True:
    try:
        coordinates = get_coordinates_and_validate()

        json = get_json_from_api(coordinates)

        # Run on the information in json and retrieve data like date and time of saturday

        saturday_times = get_times_from_json(json["items"])

        print_times(saturday_times)

    except KeyError or ValueError:  # If the input is incorrect, it will receive another input
        print("Problem reading the data ,try new input")
    except Exception:  # If it's another error, try running a few more times
        print("Something went wrong ,try again")
    else:  # If no error finish the program
        break
