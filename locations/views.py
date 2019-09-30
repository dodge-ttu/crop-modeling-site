import time
from itertools import accumulate
from django.shortcuts import render
from locations.models import Location
from metload.models import Obsset
from datetime import datetime, timedelta
from ETo_py.eto import EToEstimator


def gdu_calc(temp_c, gdu_base=15.6, gdu_max=38.0, day_fraction=(1/48)):
    if temp_c > gdu_max:
        temp_c = gdu_max

    heat_units = temp_c - gdu_base

    if heat_units < 0:
        heat_units = 0

    heat_units = heat_units * day_fraction

    return heat_units


def single_location(**kwargs):

    location = kwargs['location']
    selectstartdate = kwargs['selectstartdate']
    selectenddate = kwargs['selectenddate']
    gdu_base = kwargs['gdu_base']
    gdu_max = kwargs['gdu_max']

    if selectstartdate and selectenddate:
        selectstartdate_tup = datetime.strptime(selectstartdate, "%m/%d/%Y").timetuple()
        selectenddate_tup = datetime.strptime(selectenddate, "%m/%d/%Y").timetuple()
        start_stamp = time.mktime(selectstartdate_tup)
        end_stamp = time.mktime(selectenddate_tup)

        obsn_set = list(Obsset.objects.filter(site_name=location)
                                      .filter(datetime__gte=start_stamp)
                                      .filter(datetime__lte=end_stamp).order_by('datetime'))

    else:
        ten_days_ago = time.time() - (10 * 24 * 60 * 60)
        obsn_set = list(Obsset.objects.filter(site_name=location)
                                      .filter(datetime__gte=ten_days_ago).order_by('datetime'))

    timestamps = [ob.datetime for ob in obsn_set]
    dtme = [datetime.fromtimestamp(ob.datetime) for ob in obsn_set]
    dtme = [datetime.strftime(dt, '%m-%d %H:%M') for dt in dtme]
    temps = [float(ob.temperature) for ob in obsn_set]
    temps_c = [(temp - 32) * (5 / 9) for temp in temps]

    if gdu_base and gdu_max:
        gdu_base = float(gdu_base)
        gdu_max = float(gdu_max)
        gdus = [gdu_calc(t, gdu_base=gdu_base, gdu_max=gdu_max) for t in temps_c]

    else:
        gdus = [gdu_calc(t) for t in temps_c]

    current_gdu_sum = sum(gdus)
    winds = [float(ob.wind_speed) for ob in obsn_set]
    humiditys = [float(ob.humidity) for ob in obsn_set]
    pressures = [float(ob.pressure) for ob in obsn_set]
    rains_1h = [float(ob.rain_1h) for ob in obsn_set]
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
            'utc_offset': 0,
            'print_switch': False,
            'crop_height': 50,
        }

        hist_eto_estimate = EToEstimator(**current_obs)
        hist_eto_estimate.estimate_eto()
        eto_estimate_instances.append(hist_eto_estimate)

    eto_estimate = eto_estimate_instances[-1]

    # Historical data
    context = dict()
    context['current_location'] = location
    context['selectstartdate'] = selectstartdate
    context['selectenddate'] = selectenddate
    context['datetimehist'] = dtme
    context['temphist'] = temps
    context['temphist_c'] = temps_c
    context['windhist'] = winds
    context['presshist'] = pressures
    context['rains_1hhist'] = rains_1h
    context['gdushist'] = [round(n,3) for n in gdus]
    context['etohist'] = [round(eto.eto,3) for eto in eto_estimate_instances]
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
    context['accum_etohist'] = [round(i, 3) for i in accumulate(context['etohist'])]
    context['accum_gduhist'] = [round(i, 3) for i in accumulate(context['gdushist'])]

    # Current obs
    context['current_wind_speed'] = current_wind_speed
    context['current_temp'] = current_temp
    context['current_temp_c'] = current_temp_c
    context['current_humidity'] = current_humidity
    context['current_pressure'] = current_pressure
    context['current_period_begin'] = "{0:.1f}".format(eto_estimate.clock_at_beginning)
    context['current_period_end'] = "{0:.1f}".format(eto_estimate.clock_at_end)
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
    context['current_gdu_sum'] = round(current_gdu_sum, 3)
    context['current_eto_sum'] = round(sum(context['etohist']), 3)
    context['current_rain_sum'] = round(sum(context['rains_1hhist']), 3)
    context['current_water_deficit'] = round((context['current_eto_sum']-context['current_rain_sum']), 3)
    context['gdu_base'] = gdu_base
    context['gdu_max'] = gdu_max

    return context


def index(request):

    location = request.GET.get('location', None)
    selectstartdate = request.GET.get('selectstartdate', None)
    selectenddate = request.GET.get('selectenddate', None)
    gdu_base = request.GET.get('gdu_base', None)
    gdu_max = request.GET.get('gdu_max', None)

    params = {
        'location': location,
        'selectstartdate': selectstartdate,
        'selectenddate': selectenddate,
        'gdu_base': gdu_base,
        'gdu_max': gdu_max,
    }

    #print(location, selectstartdate, selectenddate, gdu_base, gdu_max)

    # Single Location.
    if location is not None:

        context = single_location(**params)

        return render(request, 'locations/location.html', context)

    # Initial page.
    else:
        # Get locations from db.
        locations = Location.objects.all()
        selectstartdate_tup = datetime.now() - timedelta(days=10)
        selectenddate_tup = datetime.now()
        start_stamp = time.mktime(selectstartdate_tup.timetuple())
        end_stamp = time.mktime(selectenddate_tup.timetuple())

        # Prepare current temp data for google map layer js.
        obs_sets = []
        for loc in locations:
            print(loc)
            observations = Obsset.objects.filter(location=loc).filter(datetime__gte=start_stamp). \
                filter(datetime__lte=end_stamp).order_by('datetime')
            observations = list(observations)
            temps = [float(ob.temperature) for ob in observations]
            temp = temps[-1]
            info_dict = {'temp': temp, 'loc': loc.name}
            obs_sets.append(info_dict)

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
            'obs_set': obs_sets,
        }

        return render(request, 'locations/index.html', context)
