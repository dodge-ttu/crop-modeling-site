from django.shortcuts import render
from locations.models import Location
from metload.models import Obsset
from datetime import datetime, timedelta
from ETo_py.eto import EToEstimator


def index(request):

    # Get location.
    if 'location' in request.GET:

        location = request.GET['location']
        obsn_set = list(Obsset.objects.filter(site_name=location).reverse())
        timestamps = [ob.datetime for ob in obsn_set]
        dtme = [(datetime.fromtimestamp(ob.datetime) - timedelta(hours=5)) for ob in obsn_set]
        dtme = [datetime.strftime(dt, '%m-%d %H:%M') for dt in dtme]
        temps = [float(ob.temperature) for ob in obsn_set]
        temps_c = [(temp - 32)*(5/9) for temp in temps]
        winds = [float(ob.wind_speed) for ob in obsn_set]
        humiditys = [float(ob.humidity) for ob in obsn_set]
        pressures = [float(ob.pressure) for ob in obsn_set]
        latitude = obsn_set[0].latitude
        longitude = obsn_set[0].longitude
        current_temp = temps[-1]
        current_temp_c = temps_c[-1]
        current_wind_speed = winds[-1]
        current_humidity = humiditys[-1]
        current_pressure = pressures[-1]

        eto_estimate_instances = []
        for (temp, wind, press, rh, tstmp) in zip(temps_c, winds, pressures, humiditys, timestamps):

            current_obs = {
                'latitude': float(latitude),
                'longitude': float(longitude),
                'air_temp': temp,
                'air_temp_min': temp,
                'air_temp_max': temp,
                'wind_speed': wind * 0.44704,  # convert to meters per seconds
                'relative_humidity': rh / 100,  # convert to a percentage
                'pressure': press * .1,  # convert millibars to kPa
                'period_length': 30,
                'utc_offset': 5,
            }

            hist_eto_estimate = EToEstimator(**current_obs)
            hist_eto_estimate.estimate_eto()
            eto_estimate_instances.append(hist_eto_estimate)

        eto_estimate = eto_estimate_instances[-1]

        # Historical data
        context = dict()
        context['datetimehist'] = dtme
        context['temphist'] = temps
        context['temphist_c'] = temps_c
        context['windhist'] = winds
        context['presshist'] = pressures
        context['etohist'] = [eto.eto for eto in eto_estimate_instances]
        context['etsolarradhist'] = [eto.r_a for eto in eto_estimate_instances]
        context['solradhist'] = [eto.r_s for eto in eto_estimate_instances]
        context['clearskyhist'] = [eto.r_so for eto in eto_estimate_instances]
        context['shortwavehist'] = [eto.r_ns for eto in eto_estimate_instances]
        context['satvaphist'] = [eto.e_deg_t for eto in eto_estimate_instances]
        context['slopesatvaphist'] = [eto.d for eto in eto_estimate_instances]
        context['actvaphist'] = [eto.e_a for eto in eto_estimate_instances]
        context['psychroconsthist'] = [eto.y for eto in eto_estimate_instances]
        context['netlonwavehist'] = [eto.r_n for eto in eto_estimate_instances]
        context['soilheatfluxhist'] = [eto.g for eto in eto_estimate_instances]

        # Current obs
        context['current_wind_speed'] = current_wind_speed
        context['current_temp'] = current_temp
        context['current_temp_c'] = current_temp_c
        context['current_humidity'] = current_humidity
        context['current_pressure'] = current_pressure
        context['current_period_begin'] = "{0:.2f}".format(eto_estimate.clock_at_beginning)
        context['current_period_end'] = "{0:.2f}".format(eto_estimate.clock_at_end)
        context['current_eto'] = round(eto_estimate.eto, 3)
        context['current_et_solar_rad'] = round(eto_estimate.r_a, 3)
        context['current_solar_rad'] = round(eto_estimate.r_s, 3)
        context['current_clear_sky_rad'] = round(eto_estimate.r_so, 3)
        context['current_shortwave_rad'] = round(eto_estimate.r_ns, 3)
        context['current_sat_vap_pressure'] = round(eto_estimate.e_deg_t, 3)
        context['current_slope_sat_vap_pressure'] = round(eto_estimate.d, 3)
        context['current_actual_vapor_pressure'] = round(eto_estimate.e_a, 3)
        context['psychrometric_constant'] = round(eto_estimate.y, 3)
        context['net_longwave_radiation'] = round(eto_estimate.r_n, 3)
        context['soil_heat_flux'] = round(eto_estimate.g, 3)

        return render(request, 'locations/location.html', context)

    # Initial page.
    else:
        # Get locations from db.
        locations = Location.objects.all()

        # Prepare locations dictionary for google map layer js.
        locs_ls = []
        for loc in locations:
            lat = loc.latitude
            lon = loc.longitude
            name = loc.name
            site_id = loc.site_id

            locs_ls.append({'site_id': site_id, 'name': name, 'lat': lat, 'lon': lon})
        
        context = {
            'locs_ls': locs_ls,
        }

        return render(request, 'locations/index.html', context)
