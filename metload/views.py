import logging
from django.shortcuts import render
from metload.models import Obsset
from locations.models import Location
from metload.owm_get_region import region_info, parse_met_vars
logger = logging.getLogger(__name__)
print(__name__)

with open('/home/will/crop-modeling-site/metload/met_load_key.txt') as f:
    MET_KEY = f.read().splitlines()[0] # strip newlines

with open('/home/will/crop-modeling-site/metload/owm_api_key.txt') as f:
    API_KEY = f.read().splitlines()[0] # strip newlines


def obsload(request, api_key=API_KEY, met_key=MET_KEY):
    if met_key in request.GET:
        print('[INFO] Getting met data from OWM')

        appid = api_key
        latitude = 33.577862
        longitude = -101.855171
        count = 50

        params = {
            'lat': latitude,
            'lon': longitude,
            'city_count': count,
            'APPID': appid,
            'units': 'imperial',
        }

        region_data_and_info, data_request_time = region_info(**params)
        message = region_data_and_info['message']
        cod = region_data_and_info['cod']
        count = region_data_and_info['count']
        my_list = region_data_and_info['list']
        logger.warning(f'[INFO] Message:{message}')
        print(f'[INFO] Response code:{cod}')
        print(f'[INFO] Response count:{count}')
        for l in my_list:
            print(f"[INFO] ID: {l['id']}  Lat:{l['coord']['lat']:.4f}  Lon:{l['coord']['lon']:.4f}  Name: {l['name']}")

        cln_obs_data_all_sites = parse_met_vars(region_data_and_info)

        for cln_obs_data in cln_obs_data_all_sites.values():

            obs = Obsset(
                    location=Location.objects.get(name=cln_obs_data['site_name']),
                    quality_message=cln_obs_data['quality_message'],
                    datetime=cln_obs_data['datetime'],
                    cod=cln_obs_data['cod'],
                    city_count=cln_obs_data['city_count'],
                    site_id=cln_obs_data['site_id'],
                    site_name=cln_obs_data['site_name'],
                    latitude=cln_obs_data['lat'],
                    longitude=cln_obs_data['lon'],
                    sunrise=cln_obs_data['sunrise'],
                    sunset=cln_obs_data['sunset'],
                    temperature=cln_obs_data['temp'],
                    pressure=cln_obs_data['pressure'],
                    humidity=cln_obs_data['humidity'],
                    temp_min=cln_obs_data['temp_min'],
                    temp_max=cln_obs_data['temp_max'],
                    wind_speed=cln_obs_data['wind_speed'],
                    wind_dir=cln_obs_data['wind_dir'],
                    wind_gust=cln_obs_data['wind_gust'],
                    rain_1h=cln_obs_data['rain_1h'],
                    rain_3h=cln_obs_data['rain_3h'],
                    snow=cln_obs_data['snow'],
                    weather_id=cln_obs_data['weather_id'],
                    weather_main=cln_obs_data['weather_main'],
                    weather_desc=cln_obs_data['weather_desc'],
                    weather_icon=cln_obs_data['weather_icon'],
                    st_clouds=cln_obs_data['st_clouds'],
            )

            obs.save()

        context = {'message': 'success'}

        return render(request, 'metload/index.html', context)

    else:

        context = {'message': 'denied'}

        return render(request, 'metload/index.html', context)

if __name__ == '__main__':

    with open('/home/will/crop-modeling-site/metload/met_load_key.txt') as f:
        MET_KEY = f.read().splitlines()[0] # strip newlines

    with open('/home/will/crop-modeling-site/metload/owm_api_key.txt') as f:
        API_KEY = f.read().splitlines()[0] # strip newlines

    obsload(request, api_key=API_KEY, met_key=MET_KEY)
