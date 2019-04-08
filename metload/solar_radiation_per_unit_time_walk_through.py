# This is a walk-through describing a method to calculate solar radiation for a given sub-day time
# interval. The method is documented on the FAO website for ETo calculation found at the link below:
#
# http://www.fao.org/3/X0490E/x0490e07.htm#solar%20radiation
#
# Notation and explanation has been taken directly from the link above.
#
# Extraterrestrial radiation for hourly or shorter periods (R_a)
#
# For hourly or shorter time periods the solar time angle at the beginning and end of the period
# the period should be considered when calculating R_a:
#
# R_a = (12(60) / π) * G_sc * d_r * ( (ω_2 - ω_1) * sin(φ) * sin(𝛿) + cos(φ) + cos(𝛿) * (sin(ω_2) - sin(ω_1) )
#
# R_a: extraterrestrial radiation in the hour (or shorter) period [MJ m^-2 hour^-1]
# G_sc: solar constant = 0.0820 MJ m^-2 min^-1
# d_r: inverse relative distance Earth-Sun
# 𝛿: solar declination (will be termed "little_delta" below)
# j: latitude in (j is φ but is denoted as j in the notes on the FAO link above)
# d: solar decimation
# ω_1: solar time angle at beginning of period
# ω_2: solar time angle at end of period

import math
from datetime import datetime, timedelta

# Calculate inverse relative distance Earth-Sun
j = math.radians(33.576698)
d_r = 1 + 0.033 * math.cos(((2*math.pi)/365)*j)

# Calculate solar declination
little_delta = 0.409 * math.sin((((2*math.pi)/365)*j)-1.39)

# Calculate the solar time angle at the midpoint of the period.
#
# ω = (π/12) * ( t + ( 0.0667 * (L_z - L_m) + S_o) - 12 )
#
# t: standard clock time at the midpoint of the period (hour). For example for a period between 14.00 and 15.00 hours
#    the value for t 14.50
# L_z: longitude of the center of the local time zone (degrees west of Greenwich) -97.138451 for central US time zone. (Winnipeg, Canada)
# L_m: longitude of the measurement site -101.855072 for Lubbock TX
# S_c: seasonal correction for solar time

# The seasonal correction for solar time
#
# S_c = 0.1645 * sin(2*b) - 0.1255 * cos(b) - 0.025 * sin(b)
# b = ((2 * π) * (day_of_year-81)) / 364

# Seasonal correction for solar time
day_of_year = datetime.now().timetuple().tm_yday
b = ((2*math.pi)*(day_of_year-81)) / 364
S_c = 0.1645 * math.sin(2*b) - 0.1255 * math.cos(b) - 0.025 * math.sin(b)

# Solar time angle at the midpoint of the period
# Because the met data I'm harvesting is collected every thirty minutes I need a function to return the current
# time rounded to the 15 minutes or 45 minutes depending on weather the current time is above or below the half hour
# mark.

def get_midpoint_period(UTC_offset=5):
    time_now = datetime.now() - timedelta(hours=UTC_offset)
    time_now = time_now.timetuple()

    if time_now.tm_min < 30:
        clock_at_midpoint = time_now.tm_hour + 0.25

    else:
        clock_at_midpoint = time_now.tm_hour + .75

    return clock_at_midpoint

t = get_midpoint_period()

# Solar time angle at midpoint of period
L_z = -97.138451
L_m = -101.855072
little_omega = (math.pi/12)*(t + (0.06667*(L_z - L_m) + S_c) - 12)

# Solar time angle at the beginning and end of the period
t_1 = 0.5 # This is the length of the calculation period 1 for hour 0.5 for thirty minutes
little_omega_1 = little_omega - ((math.pi*t_1)/24)
little_omega_2 = little_omega + ((math.pi*t_1)/24)

# Extraterrestrial radiation for hourly or shorter period
G_sc = 0.0820 # MJ * m^-2 * min^-1
R_a = ((12*(60))/math.pi)*G_sc*d_r*((little_omega_2-little_omega_1)*(math.sin(j)*math.sin(little_delta))+(math.cos(j)*math.cos(little_delta)*(math.sin(little_omega_2)-math.sin(little_omega_1))))