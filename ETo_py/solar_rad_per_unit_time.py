import math
from datetime import datetime, timedelta


def get_midpoint_period(period_length=30, UTC_offset=5):
    """
    This function will grab the current time and return a midpoint for a given period in terms of hours as a float.
    If the period length is thirty minutes and the current time is 12:04 then the function will return 12.25 which is
    equal to 12:15 or the midpoint of a thirty minute period from 12:00 to 12:30. This value is necessary to estimate
    solar radiation for the given period length.

    :param period_length: a length of time in minutes
    :param UTC_offset: offset in hours to local time from UTC
    :return: midpoint in terms of hours as float (0-24)
    """

    time_now = datetime.now() - timedelta(hours=UTC_offset)
    time_now = time_now.timetuple()

    if time_now.tm_min < period_length:
        clock_at_midpoint = time_now.tm_hour + 0.25

    else:
        clock_at_midpoint = time_now.tm_hour + .75

    return clock_at_midpoint


def et_solar_rad(latitude=33.576698):
    """
    Estimate extraterrestrial solar radiation. Extraterrestrial radiation is the radiation that strikes a plane
    perpendicular to the Sun's rays at the top of the Earth's atmosphere. This is the major energy source driving
    evapotranspiraton.

    :param latitude: latitude for location where
    :return: extraterrestrial radiation for the given period [MJ m^-2 hour^-1]
    """

    # Calculate inverse relative distance Earth-Sun
    j = math.radians(latitude)
    d_r = 1 + 0.033 * math.cos(((2*math.pi)/365)*j)

    # Calculate solar declination
    little_delta = 0.409 * math.sin((((2*math.pi)/365)*j)-1.39)

    # Seasonal correction for solar time
    day_of_year = datetime.now().timetuple().tm_yday
    b = ((2*math.pi)*(day_of_year-81)) / 364
    S_c = 0.1645 * math.sin(2*b) - 0.1255 * math.cos(b) - 0.025 * math.sin(b)

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

    return R_a

