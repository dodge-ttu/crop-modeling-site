import math
from datetime import datetime, timedelta


def sun_rise_set(latitude=33.576698, longitude=-101.855072, UTC_offset=5):
    """ This is a function that will calculate sunrise and sunset from a given latitude and current time. The method
    for deriving sunrise and sunset from geolocation and Julian date was taken from the following Wikipedia page:

    https://en.wikipedia.org/wiki/Sunrise_equation

    :param latitude: Latitude in decimal degrees with default for Lubbock, TX
    :param longitude: Longitude in decimal degrees with default for Lubbock, TX
    :UTC_offset: Offset for location from UTC
    :return: sunrise and sunset times
    """

    # The calculation below simply find the difference between now and Jan 1, 2000 12:00 an adds leap seconds.
    J_yr_2000 = 2451545.0

    origin = datetime.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
    time_now = datetime.now() # Server in UTC so subtract 5 hrs for Lubbock TX

    # Difference between now and Jan 1, 2000 12:00.
    time_diff = time_now - origin

    n = time_diff.days

    # Calculate mean solar noon.
    l_w = longitude

    J_approx = n - (l_w / 360)

    # Calculate solar mean anomaly
    M = (357.5291 + 0.98560028 * J_approx) % 360

    M = math.radians(M)

    # Calculate the Equation of the center
    C = (math.radians(1.9148) * math.sin(M) )+ (math.radians(0.0200) * math.sin(2*M)) + (math.radians(0.0003) * math.sin(3*M))

    C = math.degrees(C)
    M = math.degrees(M)

    # Calculate the ecliptic longitude
    eclipt_long = (M + C + 180 + 102.9372) % 360

    # Calculate solar transit
    eclipt_long = math.radians(eclipt_long)
    M = math.radians(M)

    J_transit = J_yr_2000 + J_approx + (math.radians(0.0053) * math.sin(M)) - (math.radians(0.0069) * math.sin(2 * eclipt_long))

    # Calculate the declination of the sun.
    little_delta = math.asin((math.sin(eclipt_long) * math.sin(math.radians(23.44))))

    # Calculate the hour angle
    phi = latitude

    w_naught = math.acos((math.sin(math.radians(-0.83)) - (math.sin(math.radians(phi)) * math.sin(little_delta))) / (math.cos(math.radians(math.radians(phi))) * math.cos(little_delta)))

    # Calculate sunrise and sunset
    w_naught = math.degrees(w_naught)

    J_rise = J_transit - (w_naught / 360)
    J_set = J_transit + (w_naught / 360)

    sunrise = J_rise - 2451545.0
    sunset = J_set - 2451545.0

    todays_sunrise = (origin + timedelta(days=sunrise)) - timedelta(hours=UTC_offset)
    todays_sunset = (origin + timedelta(days=sunset)) - timedelta(hours=UTC_offset)

    return (todays_sunrise, todays_sunset)