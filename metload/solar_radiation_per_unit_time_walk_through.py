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
# 𝛿: solar declination
# j: latitude in (j is φ but is denoted as j in the notes on the FAO link above)
# d: solar decimation
# ω_1: solar time angle at beginning of period
# ω_2: solar time angle at end of period

# Calculate inverse relative distance Earth-Sun



