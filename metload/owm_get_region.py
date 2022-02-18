import requests
from datetime import datetime as dt
from metload.sunrise_sunset import sun_rise_set

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

    # Calculation for sunrise and sunset is includes here based on the center point for the region.
    tdy_sunrise, tdy_sunset = sun_rise_set(latitude=33.576698, longitude=-101.855072, UTC_offset=5)
    tdy_sunrise = tdy_sunrise.timestamp()
    tdy_sunset = tdy_sunset.timestamp()

    cln_obs = {}

    for st in met:

        st_id = st['id']
        st_name = st['name']
        st_coords = st['coord']
        st_main = st['main']
        st_dt = st['dt']
        st_wind = st['wind']
        st_sys = st['sys'] # OWM internal parameters, but sunrise and sunset is included here
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
            'sunrise': tdy_sunrise if tdy_sunrise else 'NaN',
            'sunset': tdy_sunset if tdy_sunset else 'Nan',
            'temp': st_main['temp'] if 'temp' in st_main else 'NaN',
            'pressure': st_main['pressure'] if 'pressure' in st_main else 'NaN',
            'humidity': st_main['humidity'] if 'humidity' in st_main else 'NaN',
            'temp_min': st_main['temp_min'] if 'temp_min' in st_main else 'NaN',
            'temp_max': st_main['temp_max'] if 'temp_max' in st_main else 'NaN',
            'datetime': st_dt if st_dt else 'NaN',  # datetime in unix, UTC
            'wind_speed': st_wind['speed'] if 'speed' in st_wind else 'NaN',
            'wind_dir': st_wind['deg'] if 'deg' in st_wind else 'NaN',
            'wind_gust': st_wind['gust'] if 'gust' in st_wind else 'NaN',
            'rain_1h': st_rain['1h'] if st_rain and ('1h' in st_rain) else 0,
            'rain_3h': st_rain['3h'] if st_rain and ('3h' in st_rain) else 0,
            'snow': st_snow if st_snow else 0,
            'weather_id': st_weather[0]['id'] if 'id' in st_weather[0] else 'NaN',
            'weather_main': st_weather[0]['main'] if 'main' in st_weather[0] else 'NaN',
            'weather_desc': st_weather[0]['description'] if 'description' in st_weather[0] else 'NaN',
            'weather_icon': st_weather[0]['icon'] if 'id' in st_weather[0] else 'NaN',
            'st_clouds': st_clouds['all'] if 'all' in st_clouds else 'NaN',
        }

        cln_obs[st_name] = st_dict

    return cln_obs


#if __name__ == '__main__':
#    
#    with open('/home/will/crop-modeling-site/metload/owm_api_key.txt') as f:
#        API_KEY = f.read().splitlines()[0]
#
#        appid = API_KEY
#        latitude = 33.577862
#        longitude = -101.855171
#        count = 50
#
#        params = {
#            'lat': latitude,
#            'lon': longitude,
#            'city_count': count,
#            'APPID': appid,
#            'units': 'imperial',
#        }
#
#        region_data_and_info, data_request_time = region_info(**params)
#        #{'message': 'accurate', 'cod': '200', 'count': 50, 'list': [{'id': 5525577, 'name': 'Lubbock', 'coord': 
#        message = region_data_and_info['message']
#        cod = region_data_and_info['cod']
#        count = region_data_and_info['count']
#        my_list = region_data_and_info['list']
#        print(f'[INFO] Message:{message}')
#        print(f'[INFO] Response code:{cod}')
#        print(f'[INFO] Response count:{count}')
#        for l in my_list:
#            print(f"[INFO] ID: {l['id']}  Lat:{l['coord']['lat']:.4f}  Lon:{l['coord']['lon']:.4f}  Name: {l['name']}")
            






