import requests
from datetime import datetime as dt
<<<<<<< HEAD

=======
from metload.sunrise_sunset import sun_rise_set
>>>>>>> e37ae9a73216b904bbc3d6f88d8398f75c672ef5

def region_info(lat, lon, city_count, APPID, units):
    """ Return current weather observation data for a number of cities about an origin.

    :param lat: Center latitude.
    :param lon: Center longitude.
    :param city_count: Number of cities around the center that should be returned. Max is 50.
    :param APPID: Open Weather Map app ID from developer registration.
    :param units: Observation value units, 'metric', 'imperial'.
    :return: JSON from Open Weather Map request.
    """

    payload = {
        'lat': lat,
        'lon': lon,
        'cnt': city_count,
        'APPID': APPID,
        'units': units,
    }

    request_time = dt.now()
    print('[INFO] Data requested on: {}'.format(request_time))

    data = requests.get('https://api.openweathermap.org/data/2.5/find', params=payload)
    data = data.json()

    return (data, request_time)


def parse_met_vars(owm_data):
    """ Consolidate the Open Weather Map response json data into a single dictionary with met variables.

    :param owm_data: The JSON response for a region.
    :return: A dictionary of organized weather data for a single observation for all cities.
    """

    message = owm_data['message'] # Observation characterization
    cod = owm_data['cod'] # Internal parameter
    count = owm_data['count'] # Number of cities in data
    met = owm_data['list'] # Weather data for all cites

<<<<<<< HEAD
=======
    # Calculation for sunrise and sunset is includes here based on the center point for the region.
    tdy_sunrise, tdy_sunset = sun_rise_set(latitude=33.576698, longitude=-101.855072, UTC_offset=5)
    tdy_sunrise = tdy_sunrise.timestamp()
    tdy_sunset = tdy_sunset.timestamp()

>>>>>>> e37ae9a73216b904bbc3d6f88d8398f75c672ef5
    cln_obs = {}

    for st in met:
        st_id = st['id']
        st_name = st['name']
        st_coords = st['coord']
        st_main = st['main']
        st_dt = st['dt']
        st_wind = st['wind']
<<<<<<< HEAD
        st_sys = st['sys'] # OWM internal parameters, but sunrise and sunset is included here
=======
        # st_sys = st['sys'] # OWM internal parameters
>>>>>>> e37ae9a73216b904bbc3d6f88d8398f75c672ef5
        st_rain = st['rain']
        st_snow = st['snow']
        st_clouds = st['clouds']
        st_weather = st['weather']

        st_dict = {
            'quality_message': message if message else 'NaN',
            'cod': cod if cod else 'NaN',
            'city_count': count if count else 'NaN',
            'site_id': st_id if st_id else 'NaN',
            'site_name': st_name if st_name else 'NaN',
            'lat': st_coords['lat'] if st_coords else 'NaN',
            'lon': st_coords['lon'] if st_coords else 'NaN',
<<<<<<< HEAD
            'sunrise':st_sys['sunrise'] if ('sunrise' in st_sys) else 'NaN',
            'sunset':st_sys['sunset'] if ('sunset' in st_sys) else 'Nan',
=======
            'sunrise':tdy_sunrise if tdy_sunrise else 'NaN',
            'sunset':tdy_sunset if tdy_sunset else 'Nan',
>>>>>>> e37ae9a73216b904bbc3d6f88d8398f75c672ef5
            'temp': st_main['temp'] if 'temp' in st_main else 'NaN',
            'pressure': st_main['pressure'] if 'pressure' in st_main else 'NaN',
            'humidity': st_main['humidity'] if 'humidity' in st_main else 'NaN',
            'temp_min': st_main['temp_min'] if 'temp_min' in st_main else 'NaN',
            'temp_max': st_main['temp_max'] if 'temp_max' in st_main else 'NaN',
            'datetime': st_dt if st_dt else 'NaN', # datetime in unix, UTC
            'wind_speed': st_wind['speed'] if 'speed' in st_wind else 'NaN',
            'wind_dir': st_wind['deg'] if 'deg' in st_wind else 'NaN',
            'wind_gust': st_wind['gust'] if 'gust' in st_wind else 'NaN',
<<<<<<< HEAD
            'rain_1h': st_rain['1h'] if st_rain else 0,
            'rain_3h': st_rain['3h'] if st_rain else 0,
=======
            'rain_1h': st_rain['1h'] if st_rain and ('1h' in st_rain) else 0,
            'rain_3h': st_rain['3h'] if st_rain and ('3h' in st_rain) else 0,
>>>>>>> e37ae9a73216b904bbc3d6f88d8398f75c672ef5
            'snow': st_snow if st_snow else 0,
            'weather_id': st_weather[0]['id'] if 'id' in st_weather[0] else 'NaN',
            'weather_main': st_weather[0]['main'] if 'main' in st_weather[0] else 'NaN',
            'weather_desc': st_weather[0]['description'] if 'description' in st_weather[0] else 'NaN',
            'weather_icon': st_weather[0]['icon'] if 'id' in st_weather[0] else 'NaN',
            'st_clouds': st_clouds['all'] if 'all' in st_clouds else 'NaN',
        }

        cln_obs[st_name] = st_dict

    return cln_obs
