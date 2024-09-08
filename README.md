
# WEATHER.py

#### Video Demo: <URL [Weather.py](https://youtu.be/iZX3ba_gTsY)>

#### Description:

`Weather.py` is a simple command line program that displays the weather forecast for your location. It uses various APIs to retrieve data which is then used to create a weather forecast for that specific location.

Don't get me wrong. I'm not trying to reinvent the wheel. I thought this would be a cool idea for my final CS50 Python project.

#### How does it work?

When launched, it will attempt to determine the location using an IP address or search for a location using a parameter passed on the command line. It will use `my_IP()` to get the IP address and my_location(ip) or get_latlon("search_word") to return the coordinates and address. After determining the location and determining the latitude and longitude, It will connect to the openmeteo API to find weather data for that location.

It was supposed to be a simple program for quickly checking the weather, so I decided to collect only daily data, limiting to the weather code (sun, rain, etc.) and minimum and maximum temperatures.

Of course, this API offers much more data such as pressure, air quality, UV index, etc. You can also get hourly weather and archived data from previous days.

#### Usage:

By default, it displays today's weather forecast based on your IP location.

For example, I'm from Southampton, but my ISP's IP address is in London, so if I run the program without any parameters, I should see something like this:

```
$ python weather.py

Your location is: London, GB.
Latitude: 51.5074, Longitude: -0.1196

Weather forcast for this location:
Today: Thunderstorm: Slight or moderate. Temperatures ranging from 14.5°C to 19.7°C.
```

Of course, the weather is different in different cities. If the automatic location is not accurate, you can use the `-s` parameter to search for a place.

The correct syntax is: `weather.py -s "search phrase"`, and the search phrase can be a city, country, place, postal code or just a full address. But in the case of the latter, the results may be false. To get the most accurate location possible, I advise you to limit yourself to the city and country.

For example, if I wanted to check the weather in Southampton, I could use the following syntax:

```
$ python weather.py -s "Southampton, UK"

Your location is: Southampton, England, United Kingdom.
Latitude: 50.9025, Longitude: -1.4042

Weather forcast for this location:
Today: Rain showers: Slight, moderate, and violent. Temperatures ranging from 14.9°C to 18.5°C.
```

The program allows you to display the weather for a maximum of 14 days. To do this, use the `-d` paragraph followed by number of days.

I want the weather forecast for my city of Southampton for the next 5 days. The syntax looks like this:

```
$ python weather.py -s "Southampton, UK" -d 5

Your location is: Southampton, England, United Kingdom.
Latitude: 50.9025, Longitude: -1.4042

Weather forcast for this location:
Today: Rain showers: Slight, moderate, and violent. Temperatures ranging from 14.9°C to 18.5°C.
Day 2: Mainly clear, partly cloudy, and overcast. Temperatures ranging from 12.0°C to 17.3°C.
Day 3: Rain: Slight, moderate and heavy intensity. Temperatures ranging from 11.4°C to 18.3°C.
Day 4: Mainly clear, partly cloudy, and overcast. Temperatures ranging from 8.3°C to 14.3°C.
Day 5: Mainly clear, partly cloudy, and overcast. Temperatures ranging from 7.3°C to 15.0°C.
```

The program also allows you to display location data, such as address data and coordinates. This can be done by running the program with the `-l` parameter.

This function has two modes, the first when locating using an IP address and the second when locating by search with values ​​passed from arguments.

Localisation by IP:

```
$ python weather.py -l

Your location is: London, GB.
Latitude: 51.5074, Longitude: -0.1196
```

Another way is to add the "-s" parameter in the syntax as follows:

```
$ python weather.py -s "Southampton, UK" -l

Your location is: Southampton, England, United Kingdom.
Latitude: 50.9025, longitude: -1.4042
```

And finally, the `-h` parameter, which, as usual, displays a help screen with all available parameters.

#### Tests, libraries and APIs

I used several libraries to help me with the project. One of them is geopy and uses the free Nominatim geolocation API. I used it to get the latitude and longitude which I needed later to get the weather data from another API - openmeteo.

To get the location by using IP address I used ipify and ipapi APIs, first to get IP and with this to get latitude and longitude.

To get response from APIs I used requests library except for Nominatim which was imported by geopy and works much better.

Library argparse helps to handle parameters from command line. It also handles errors related with that. To display emoji I used function emojize from emoji library.

To test the application functions, I used the pytest library and created several functions in `test_weather.py`

Here is a list of all the APIs used in this project

1. ipify: This API will help us know the IP address where the request is coming from.

2. ipapi: This API will help us retrieve the location information for a specific IP address.

3. Nominatim is a tool that allows you to search OSM data by name and address and generate synthetic addresses of OSM points (reverse geocoding).

4. Open-Meteo is an open-source weather API offering free access for non-commercial use. No API key required.
