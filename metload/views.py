from django.shortcuts import render
from metload.models import Obsset
from locations.models import Location
from metload.owm_get_region import region_info, parse_met_vars


with open('/home/will/crop_mod_site/metload/met_load_key.txt') as f:
    met_key = f.read()


def obsload(request):
    if met_key in request.GET:

        appid = '86b1c9731a07438094b67f087a4e5595'
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
