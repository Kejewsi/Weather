import argparse
from colorama import Fore, Back, Style
import emoji
from geopy.geocoders import Nominatim
import requests


def main():

    # creates parser object using argparse library, this object will handle all parameters from command line and related errors

    parser = argparse.ArgumentParser(prog='weather.py', description="Displays the weather forecast for your location", epilog="Valid syntax eg.: weather.py -s 'London, UK' -d 7")
    parser.add_argument("-d", default=1, help="Number of forecast days (by default one day, maximum is set to 14 days).", type=int)
    parser.add_argument("-s", default="", help="Search your location by typing address, place or post code (by default is checking IP location)")
    parser.add_argument("-l", default="", help="Displays your location with latitude and longitude", action='store_true')
    args = parser.parse_args()

    line()

    # Display location

    if args.l:

        # if location passed in command line

        if args.s:
            location = get_latlon(args.s)

        # if location established through IP

        else:
            ip = my_ip()
            location = my_location(ip)
        print(f" Your location is: {location['address']}. \n Latitude: {location['latitude']}, Longitude: {location['longitude']}")

    # display weather forecast

    else:

        # creates days variable (by default = 1)

        days = args.d
        if days > 14:
            days = 14

        # if days is negative exit program and print the error

        elif days <= 0:
            print("Number of days must be bigger than 0")
            exit(1)

        # if program executed with parameter -s (search)

        if args.s:

            # will try to run get_lanlon() function to get address and latitude and longitude
            # if unsucesfull will exit with error

            try:
                location = get_latlon(args.s)
            except ValueError:
                exit("Search unsucessfull")
            except AttributeError:
                exit("Could not find the place")

         # if program executed without -s parameter

        else:

            # will try to get IP using my_ip() function and collect the data about the IP location
            # if sucessfull will return address, latitude and longitude otherwise exit with error

            try:
                ip = my_ip()
                location = my_location(ip)
            except ValueError:
                print("Can't find the location")
                exit(1)

        # if available, displays your location from location dictionary, otherwise exit with error

        if location["address"]:
            print(f" Your location is: {location['address']}. \n Latitude: {location['latitude']}, Longitude: {location['longitude']}\n")
        else:
            exit("Could not find the location. Try add country in the search.")

        # check the weather and save the data in the list of dictionaries called weather
        # weather should contain date, weather_code, min and max temperatures
        # if unsucessfull will exit with error

        try:
            weather = check_weather(location['latitude'], location['longitude'], days)
        except ValueError:
            print("Can't check the weather")
            exit(1)

        # extractes data from list weather and creates separate lists with values

        date = weather["date"]
        w_code = weather["w_code"]
        t_min = weather["t_min"]
        t_max = weather["t_max"]

        # formating data for print

        leng = len(w_code)

        for i in range(leng):
            if i == 0:
                date[0] = "today"
            else:
                date[i] = f"day {i+1}"

        date[0] = "Forecast for today"

        # print data on the screen

        for i in range(leng):
            print(emoji.emojize(show_forecast(date[i], w_code[i], t_min[i], t_max[i])))

    line()

# funtion to print horizontal line

def line():
    print(Fore.GREEN + "=================================================================================================================" + Style.RESET_ALL) # prints one line just for aestethics


# function to get your IP

def my_ip():

    # function will try to get response from API server to get your IP and return the IP address
    # if unsucessfull will exit with error

    try:
        response = requests.get("https://api64.ipify.org?format=json").json()
        return response["ip"]
    except:
        exit("Can't connect with the server")


# function to get your location using IP

def my_location(ip_address):

    # function will try to get response from API server to get location of the IP provided
    # if unsucessfull will exit with error

    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
    except:
        exit("Can't connect with the server")
    else:

        # function will try to save data in dictionary and return that dictionary
        # if unsucessfull will exit with error

        try:
            location_data = {
                "address": response.get("city") + ", " + response.get("country_code"),
                "latitude": response.get("latitude"),
                "longitude": response.get("longitude")
            }

            return location_data
        except:
            exit("Can't save auto location")


# function to get your location by searching with provided phrase

def get_latlon(address):

    # creates the geopy object and then try to collect data from Mominatim API
    # if unsucessfull will exit with error

    try:
        geolocator = Nominatim(user_agent="MikeyWeather")
        location = geolocator.geocode(address, language='en')
    except:
        exit("Can get response from location API")
    else:

        # will try to save collected data to the dictionary and return that dictionary
        try:
            location_data = {
                "address":  location.address,
                "latitude": round(location.latitude, 4),
                "longitude": round(location.longitude, 4)
            }

            return location_data
        except AttributeError:
            raise exit("Could not find the place")


# function to check the weather

def check_weather(latitude, longitude, days):

    # function will try to get data from openmeteo API
    # if unsucessfull will exit with error

    try:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&forecast_days={days}").json()
    except:
        exit("Can't get weather data")

    else:

        # function will try to save selected data in the dictionary list called weather

        try:
            weather = {
                "date": response["daily"].get("time"),
                "w_code": response["daily"].get("weather_code"),
                "t_max": response["daily"].get("temperature_2m_max"),
                "t_min": response["daily"].get("temperature_2m_min")
            }
        except KeyError:
            exit("Can't save weather data")
        else:
            return weather


# function which create the forecast

def show_forecast(date, w_code, t_min, t_max):
    forecast = convert_code(w_code)

    return f" {date.capitalize()}: {forecast}. Temperatures ranging from {t_min}°C to {t_max}°C."


# function for weather code conversion to text

def convert_code(w_code):
    if w_code == 0:
        return ":sun:  Clear sky"
    elif w_code == 1 or w_code == 2 or w_code == 3:
        return ":sun_behind_small_cloud:  Mainly clear, partly cloudy, and overcast"
    elif w_code == 45 or w_code ==  48:
        return ":fog:  Fog and depositing rime fog"
    elif w_code == 51 or w_code ==  53 or w_code ==  55:
        return ":sun_behind_cloud:  Drizzle: Light, moderate, and dense intensity"
    elif w_code == 56 or w_code ==  57:
        return ":sun_behind_cloud:  Freezing Drizzle: Light and dense intensity"
    elif w_code == 61 or w_code ==  63 or w_code ==  65:
        return f":cloud_with_rain:  Rain: Slight, moderate and heavy intensity"
    elif w_code == 66 or w_code ==  67:
        return ":cloud_with_rain:  Freezing Rain: Light and heavy intensity"
    elif w_code == 71 or w_code ==  73 or w_code ==  75:
        return ":cloud_with_snow:  Snow fall: Slight, moderate, and heavy intensity"
    elif w_code == 77:
        return ":cloud_with_snow:  Snow grains"
    elif w_code == 80 or w_code == 81 or w_code ==  82:
        return ":cloud_with_rain:  Rain showers: Slight, moderate, and violent"
    elif w_code == 85 or w_code == 86:
        return ":cloud_with_snow:  Snow showers slight and heavy"
    elif w_code == 95:
        return ":cloud_with_lightning:  Thunderstorm: Slight or moderate"
    elif w_code == 96 or w_code == 99:
        return ":cloud_with_lightning_and_rain:  Thunderstorm with slight and heavy hail"
    else:
        return ":sleeping_face:  Unavailable"


# if this program was execuyted it will run function main()1

if __name__ == "__main__":
    main()
