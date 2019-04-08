# ETo calculations require a measurement of solar radiation or an estimate if not measured. Knowing the duration of
# solar radiation by calculating sunrise and sunset is the starting point for a solar radiation estimate. The
# following is a method for calculating sunrise and sunset based on the following Wikipedia page:
#
# https://en.wikipedia.org/wiki/Sunrise_equation

import math
from datetime import datetime, timedelta

# Calculate the current Julian day.
#
# n = j_date - 2451545.0 + 0.0008
#
# n: is the number of days since Jan 1, 2000 12:00
# j_date: is the Julian date
# 2451545.0: the the Julian date for Jan 1, 2000 12:00
# 0.0008: the fractional Julian Day for leap seconds and terrestrial time.
#
# The calculation below simply find the difference between now and Jan 1, 2000 12:00 an adds leap seconds.
J_yr_2000 = 2451545.0

origin = datetime.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
time_now = datetime.now() # Server in UTC so subtract 5 hrs for Lubbock TX

# Difference between now and Jan 1, 2000 12:00.
time_diff = time_now - origin

n = time_diff.days

# Calculate mean solar noon.
#
# J* = n - l_w / 360 degrees
#
# J*: an approximation of mean solar tie at n expressed as a Julian day with the day fraction.
# l_w: is the longitude west (west is negative, east is positive) of the observer on the Earth.

# Longitude for Lubbock, TX
l_w = -101.855072

J_approx = n - (l_w / 360)

# Calculate solar mean anomaly
#
# M = (357.5291 + 0.98560028 x J*) mod 360
#
# M: the solar mean anomaly used in a few of the next equations.

M = (357.5291 + 0.98560028 * J_approx) % 360

M = math.radians(M)

# Calculate the Equation of the center
#
# C = 1.9148 sin(M) + 0.0200 sin(2M) + 0.0003 sin(3M)
#
# C: the Equation of center value needed to calculate lambda in the next equation.
# 1.9148: the coefficient of the Equation of the Center for the planet the observer is on (Earth in this case)

C = (math.radians(1.9148) * math.sin(M) )+ (math.radians(0.0200) * math.sin(2*M)) + (math.radians(0.0003) * math.sin(3*M))

C = math.degrees(C)
M = math.degrees(M)

# Calculate the ecliptic longitude
#
# λ = (M + C + 180 + 102.9372) mod 360
#
# λ: the ecliptic longitude
# 102.9372: a value for the argument of perihelion

eclipt_long = (M + C + 180 + 102.9372) % 360

# Calculate solar transit
#
# J_transit = 2451545.0 + J* + 0.0053 sim M - 0.0069 sin (2λ)
#
# J_transit: the Julian date for the local true solar transit (or solar noon).
# 2451545.0: noon of the equivalent Julian year reference.
# 0.0053 sin M - 0.0069 sin (2λ) is a simplified version of the equation of time. The coefficients are
# fractional day minutes.
#
# Link explaining the equation of time concept: https://en.wikipedia.org/wiki/Equation_of_time

eclipt_long = math.radians(eclipt_long)
M = math.radians(M)

J_transit = J_yr_2000 + J_approx + (math.radians(0.0053) * math.sin(M)) - (math.radians(0.0069) * math.sin(2 * eclipt_long))

# Calculate the declination of the sun.
#
# sin 𝛿 = sin λ x sin 23.44°
#
# 𝛿 is the declination of the sun.
# 23.44° is Earth's maximum axial tilt toward sun

little_delta = math.asin((math.sin(eclipt_long) * math.sin(math.radians(23.44))))

# Calculate the hour angle
#
# cos ω o  = (sin (-0.83°) - sin(Φ) x sin(𝛿)) / cos(Φ) x cos(𝛿)
#
# ω o: is the hour angle from the observer's zenith
# Φ: the north latitude of the observer (north is positive, south is negative) on the Earth

phi = 33.576698

w_naught = math.acos((math.sin(math.radians(-0.83)) - (math.sin(math.radians(phi)) * math.sin(little_delta))) / (math.cos(math.radians(math.radians(phi))) * math.cos(little_delta)))

# Calculate sunrise and sunset
#
# J_rise = J_transit - (w_naught / 360)
# J_set = J_transit + (w_naught / 360)
#
# J_rise: the actual Julian date of sunrise
# J_set: the actual Julian date of sunset

w_naught = math.degrees(w_naught)

J_rise = J_transit - (w_naught / 360)
J_set = J_transit + (w_naught / 360)

sunrise = J_rise - 2451545.0
sunset = J_set - 2451545.0

todays_sunrise = (origin + timedelta(days=sunrise)) - timedelta(hours=5)
todays_sunset = (origin + timedelta(days=sunset)) - timedelta(hours=5)

print(datetime.strftime(todays_sunrise, "%Y-%m-%d %H:%M:%S"))
print(datetime.strftime(todays_sunset, "%Y-%m-%d %H:%M:%S"))
