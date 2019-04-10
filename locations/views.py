from django.shortcuts import render, get_object_or_404
from locations.models import Location
from metload.models import Obsset
from datetime import datetime, timedelta

def index(request):

    print('ehehe')

    # Get location.
    if 'location' in request.GET:
        location = request.GET['location']

        obsn_set = Obsset.objects.filter(site_name=location)

        temps = [float(ob.temperature) for ob in obsn_set]
        temps.reverse()

        dtme = [datetime.fromtimestamp(ob.datetime) for ob in obsn_set]
        dtme = [datetime.strftime(dt, format='%m-%d %H:%M') for dt in dtme]
        temps.reverse()

        winds = [float(ob.wind_speed) for ob in obsn_set]
        winds.reverse()

        humiditys = [float(ob.humidity) for ob in obsn_set]
        humiditys.reverse()

        pressures = [float(ob.pressure) for ob in obsn_set]
        pressures.reverse()

        current_temp = temps[0]
        current_wind_speed = winds[0]
        current_humidity = humiditys[0]
        current_pressure = pressures[0]

        context = {}

        context['datetimehist'] = dtme
        context['temphist'] = temps
        context['windhist'] = winds
        context['current_wind_speed'] = current_wind_speed
        context['current_temp'] = current_temp
        context['current_humidity'] = current_humidity
        context['current_pressure'] = current_pressure

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

            locs_ls.append({'site_id':site_id, 'name':name, 'lat':lat, 'lon':lon})
        
        context = {
            'locs_ls': locs_ls,
        }

        return render(request, 'locations/index.html', context)
