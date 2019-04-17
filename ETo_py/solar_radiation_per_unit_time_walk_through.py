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

def get_midpoint_period(period_length=30, UTC_offset=5):
    time_now = datetime.now() - timedelta(hours=UTC_offset)
    time_now = time_now.timetuple()

    if time_now.tm_min < period_length:
        clock_at_midpoint = time_now.tm_hour + 0.25

    else:
        clock_at_midpoint = time_now.tm_hour + .75

    return clock_at_midpoint

t = get_midpoint_period(UTC_offset=0)

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

# From the estimation of extraterrestrial solar radiation (R_a) the amount of solar radiation that enters the Earth's
# atmosphere (Rs) can be calculated with the Angstrom formula which relates solar radiatoin to extraterrestrial
# radiation.
#
# R_s = (a_s + b_s(n/N)) * R_a
#
# R_s: solar or shortwave radiation [MJ m^-2 given_time_period^-1]
# n: actual duration of sunshine [hour as float]
# N: maximum possible duration of sunshine [hour as float]
# n/N: relative sunshine duration []
# R_a: extraterrestrial radiation [MJ m^-2 given_time_period^-1]
# a_s: regression constant, expressing the fraction of extraterrestrial radiation reaching Earth on overcast days (n=0)
# a_s + b_s: fraction of extraterrestrial radiation reaching the earth on clear days (n=N)
#
# Where no actual solar radiation data are available and no calibration has been carried out for improved a_s and b_s
# parameters, the values a_s = 0.25 and b_s = 0.50 are recommended.
#
# Because the data we are collecting is on a sub-day (30 minute) time span we will use n/N=for this calculation.

# Calculate solar radiation
n=1
N=1
a_s = 0.25
b_s = 0.5
R_s = (a_s + (b_s*(n/N))) * R_a

# The calculation of clear-sky solar radiation (R_so) is required for computing net longwave radiation.
#
# For near sea level or when calibrated values for a_s and b_s are not available:
#
# R_so = (a_s + b_s) * R_a
#
# R_so: clear-sky solar radiation [MJ m^-2 given_time_period^-1]
# a_s + b_s: fraction of extraterrestrial radiation reaching the earth on clear-sky days (n=N)
#
# When calibrated values for a_s and b_s are not available:
#
# R_so = (0.75 + 2E-5 * z) * R_a
#
# z: location elevation above sea level [meters] 976 meters for Lubbock, TX

# Calculate clear-sky radiation
z = 976
R_so = (0.75 * ((2E-5)*z)) * R_a

# Net solar or net shortwave radiation (R_ns) is the net shortwave radiation resulting from the balance between
# incoming and reflected solar radiation. This is estimated with:
#
# R_ns = (1-a) * R_s
#
# R_ns: net solar or shortwave radiation
# a: albedo or canopy reflection coefficient, which is 0.23 for the hypothetical grass reference crop [dimensionless]
# R_s: the incoming solar radiation [MJ m^-2 given_time_period^-2]

# Calculate net solar shortwave radiation
albedo = 0.23
R_ns = (1-albedo) * R_s

# Net longwave radiation (R_nl) must be calculated. The rate
#
#
#
#
#
#
#
#

