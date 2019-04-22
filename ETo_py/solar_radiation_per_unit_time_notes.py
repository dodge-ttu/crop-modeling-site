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
# atmosphere (R_s) can be calculated with the Angstrom formula which relates solar radiation to extraterrestrial
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
R_so = (0.75 + ((2E-5)*z)) * R_a

# Net solar or net shortwave radiation (R_ns) is the net shortwave radiation resulting from the balance between
# incoming and reflected solar radiation. This is estimated with:
#
# R_ns = (1-a) * R_s
#
# R_ns: net solar or shortwave radiation
# a: albedo or canopy reflection coefficient, which is 0.23 for the hypothetical grass reference crop [dimensionless]
# R_s: the incoming solar radiation [MJ m^-2 given_time_period^-1]

# Calculate net solar shortwave radiation
albedo = 0.23
R_ns = (1-albedo) * R_s

# Net longwave radiation (R_nl) must be calculated. The rate of longwave energy emission is proportional to the
# absolute temperature of the surface raised to the fourth power. This relation is expressed quantitatively by the
# Stefan-Boltzman law. The net energy flux leaving the Earth's surface is, however, less than that emitted and given
# by the Stefan-Boltzman law due to the absorption and downward radiation from the sky. Water vapour, clouds, carbon
# dioxide and dust are absorbers and emitters of longwave radiation. Their concentrations should be known when
# assessing the net outgoing flux. As humidity and cloudiness play an important role, the Stefan-Boltzmann law is
# corrected by these two factors when estimating the net outgoing flux of longwave radiation. It is thereby assumed
# that the concentrations of the other absorbers are constant:
#
# R_nl = sb_const * ((Tmax_K**4 + Tmin_K**4)/2) * (0.34-0.14*(e_a**(1/2))) * (1.35 * (R_s / R_so) - 0.35)
#
# R_nl = net outgoing longwave radiaton [MJ m^-2 given_time_period^-1]
# sb_const: Stefan-Boltzman constant [4.903E-9 MJ K^-4 m^-2 day^-1]
# Tmax_K**4: maximum absolute temperature during the time period [K]
# Tmin_K**4: minimum absolute temperature during the time period [K]
# e_a: actual vapor pressure [kPa]
# R_s/R_so: relative shortwave radiation (limited to one)
# R_s: solar radiation [MJ m^-2 given_time_period^-1]
# R_so: clear-sky radiation [MJ m^-2 given_time_period^-1]

# Given the relative humidity the actual vapor pressure is determined as:
#
# e_a = e_deg(T_period) * (RH_period / 100)
#
# e_a: average actual vapor pressure for the given time period [kPa]
# e_deg(T_period): saturation vapor pressure at air temperature T_period [kPa]
# RH_period: average relative humidity for the period expressed as a float from zero to one

# As saturation vapor pressure is related to air temperature, it can be calculated form the air temperature. This
# relationship is represented by the following equation:
#
# e_deg(T) = 0.6108 e ((17.27 * T) / (T + 237.3))
#
# e_deg(T): saturation vapor pressure at the given air temperature T [kPa]
# T: air temperature [C]
# e: 2.7183 (base of natural logarithm) raised to the power []

# Calculate saturation vapor pressure
T = 33 # Dummy celsius value for the calculation
e_deg_T = 0.6018 * math.exp((17.27 * T) / (T+237.3))

# Calculate actual vapor pressure
RH_period = .40 # Dummy value for calculation
e_a = e_deg_T * RH_period

# Calculate net longwave radiation
sb_const = 4.903E-9
Tmin = 32 # Dummy celsius value for the calculation
Tmax = 33 # Dummy celsius value for the calculation
Tmin_K = Tmin + 273.16
Tmax_K = Tmax + 273.16

# R_nl = sb_const * ((Tmax_K**4 + Tmin_K**4)/2) * (0.34-0.14*(e_a**(1/2))) * (1.35 * (R_s / R_so) - 0.35)
R_nl = (sb_const/48) * ((Tmin_K**4 + Tmax_K**4)/2) * (0.34 - (0.14 * (math.sqrt(e_a)))) * ((1.35 * (R_s/R_so)) - 0.35)

# Net radiation (R_n) is the difference between the incoming net shortwave radiation (R_ns) and the outgoing net
# longwave radiation (R_nl) expressed as:
#
# R_n = R_ns - R_nl

# Calculate net radiation
R_n = R_ns - R_nl

# Complex models are available to describe soil heat flux. Because soil heat flux is small compared to R_n,
# particularly when the surface is covered be vegetation and calculation time steps are 24 hours or longer, a simple
# calculation procedure can be used based on the idea that the soil temperature follows the air temperature. For hourly
# (or shorter) calculations, G beneath a dense cover of grass (as one would observer in the hypothetical reference
# crop) does not correlate well with air temperature. Hourly G can be approximated during daylight periods as:
#
# Daytime: G_period = 0.1 * R_n
# Nighttime: G_period = 0.5 * R_n

# Calculate soil heat flux
G_period_day = 0.1 * R_a
G_period_night = 0.5 * R_a

# When the soil is warming the value for soil heat flux is positive and should be subtracted from net radaition (R_n)
# while estimating evapotranspiration.

