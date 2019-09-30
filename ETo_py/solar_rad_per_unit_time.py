import math
from datetime import datetime, timedelta


def get_midpoint_period(period_length=30, utc_offset=5):
    """
    This function will grab the current time and return a midpoint for a given period in terms of hours as a float.
    If the period length is thirty minutes and the current time is 12:04 then the function will return 12.25 which is
    equal to 12:15 or the midpoint of a thirty minute period from 12:00 to 12:30. This value is necessary to estimate
    solar radiation for the given period length.

    :param period_length: a length of time in minutes
    :param utc_offset: offset in hours to local time from UTC
    :return: midpoint in terms of hours as float (0-24)
    """

    time_now = datetime.now() - timedelta(hours=utc_offset)
    time_now = time_now.timetuple()

    if time_now.tm_min < period_length:
        clock_at_midpoint = time_now.tm_hour + 0.25

    else:
        clock_at_midpoint = time_now.tm_hour + .75

    return clock_at_midpoint


def et_solar_rad(latitude=33.576698, day_of_year=None):
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
    if not day_of_year:
        day_of_year = datetime.now().timetuple().tm_yday

    b = ((2*math.pi)*(day_of_year-81)) / 364
    S_c = 0.1645 * math.sin(2*b) - 0.1255 * math.cos(b) - 0.025 * math.sin(b)

    t = get_midpoint_period(utc_offset=0)

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


def solar_radiation(R_a, n=1, N=1, a_s=0.25, b_s=0.5):
    """
    The portion of the extraterrestrial radiation that penetrates the atmosphere is denoted as R_s. The relationship
    between R_a and R_s can be expressed with the Angstrom formula: R_s = (a_s + b_s(n/N)) * R_a. Because this function
    is built for sub-day time spans relative sunshine duration (n/N) is set to one.

    The default values for the amount of R_a that reach Earth on overcast and clear-sky days has been set to a default
    of 0.25 and 0.5 respectively as per FAO-56 recommendation. These parameters can me adjusted based on local
    experimental data however.

    :param n: actual duration of sunshine [hour as float]
    :param N: max possible duration of sunshine [hour as float]
    :param a_s: regression constant, the fraction of R_a that reaches Earth on overcast day (n=0)
    :param b_s: fraction of R_a that reaches Earth on clear days (n=N)
    :param R_a: extraterrestrial solar radiation [MJ m^-2 given_time_period^-1]
    :return: solar radiation (R_s) [MJ m^-2 given_time_period^-1]
    """

    R_s = (a_s + (b_s*(n/N))) * R_a

    return R_s


def clear_sky_radiation(R_a, a_s=0.75, b_s=2E-5, z=976):
    """
    The calculation of clear-sky radiation is requisite in the estimation of net longwave radiation. This calculation
    requires a_s and b_s which can be calibrated through experimentation.

    In cases where calibration data are not available a value of 0.75 can be used for a_s and 2E-5 for b_s.

    :param a_s: regression constant, the fraction of R_a that reaches Earth on overcast day (n=0)
    :param b_s: fraction of R_a that reaches Earth on clear days (n=N)
    :param z: location elevation in meters, 976 for Lubbock, TX
    :param R_a: extraterrestrial solar radiation [MJ m^-2 given_time_period^-1]
    :return: clear-sky radiation (R_so) [MJ m^2 given_time_period^-1]
    """

    R_so = (a_s + (b_s * z)) * R_a

    return R_so


def net_shortwave_radiation(R_s, albedo=0.23):
    """
    Net shortwave radiation (R_ns) results from the balance between incoming and reflected solar radiation as
    described by: R_ns = (1-albedo) * R_s

    :param R_s: the incoming solar radiation [MJ m^-2 given_time_period^-1]
    :param albedo: canopy reflection for the hypothetical reference crop [dimensionless]
    :return: net solar shortwave radiation [MJ m^-2 given_time_period^-1]
    """

    R_ns = (1-albedo) * R_s

    return R_ns


def saturated_vap_pressure(air_temp=33):
    """
    A calculation a saturation vapor pressure based on air temperature as expressed by:
    e_deg_T = 0.6108 e ((17.27 * T) / (T + 237.3))

    :param air_temp: air temperature [celsius]
    :return: saturation vapor pressure at the given temperature [kPa]
    """

    e_deg_T = 0.6018 * math.exp((17.27 * air_temp) / (air_temp + 237.3))

    return e_deg_T


def slope_sat_vap_pressure(e_deg_T, T_period):
    """
    The relationship between saturation vapor pressure and temperature (D) is required in the calculation
    of evapotranspiration. The slope of this curve is given by: D = (4098 * e_deg_T) / (T + 237.3)

    :param e_deg_T: saturation vapor pressure [kPa]
    :param T_period: mean temperature for the given time period [C]
    :return: slope of saturation vapor pressure curve at air temperature T [kPa C^-1]
    """

    D = (4098 * e_deg_T) / ((T_period + 237.3)**2)

    return D


def actual_vap_pressure(e_deg_T, relative_humidity=.42):
    """
    A calculation of actual vapor pressure based on current saturation vapor pressure and relative humidity.

    :param e_deg_T: The current saturation vapor pressure at the given temperature [kPa]
    :param relative_humidity: relative humidity expressed as a float between zero and one
    :return: actual vapor pressure at the given RH [kPa]
    """

    e_a = e_deg_T * relative_humidity

    return e_a


def psychrometric_constant(pressure, c_p=1.1013E-3, latent_heat=2.45, e_ratio=0.622):
    """
    The psychrometric constant relates the partial pressure of water in the air to the air temperature.

    :param pressure: atmospheric pressure [kPa]
    :param c_p: specific heat at a constant pressure [MJ kg^-1 C^-1]
    :param latent_heat: the latent heat of vaporization, 2.45 [MJ kg^-1]
    :param e_ratio: the ratio of molecular weight of water vapor to dry air = 0.622
    :return: psychrometric constant [kPa C^-1]

    The specific heat at constant pressure is the amount of energy required to increase the temperature of a unit mass
    of air by one degree at constant pressure. This value depends on the composition of the air, i.e, on humidity.
    """

    y = (c_p * pressure) / (e_ratio * latent_heat)

    return y


def net_longwave_radiation(e_a, R_s, R_so, sb_const=4.903E-9, Tmin=32, Tmax=33):
    """
    The outgoing net longwave radiation must be calculated to estimate the radiation energy balance. The rate of
    longwave emission is proportional to the absolute temperature of the surfaces raised to the fourth power. The
    actual amount of longwave radiation leaving the Earth is less than that given by the Stefan-Boltzman law due
    to the absorption and downward radiation of the sky. Water vapor, clouds, carbon dioxide, and dust are absorbers
    and emitters of longwave radiation. Their concentrations can be known when estimation outgoing longwave flux.
    As humidiy and cloudiness play an important role, the Stefan-Boltzmann law is corrected by these two factors when
    estimating outgoing longwave radiation. The concentrations of the other absorbers are assumed to remain constant.
    This estimation takes the following form:

    R_nl = sb_const * ((Tmax_K**4 + Tmin_K**4)/2) * (0.34-0.14*(e_a**(1/2))) * (1.35 * (R_s / R_so) - 0.35)

    :param e_a: actual vapor pressure [kPa]
    :param R_s: solar radiation that enters atmosphere [MJ m^-2 given_time_period^-1]
    :param R_so: clear-sky radiation (R_so) [MJ m^2 given_time_period^-1]
    :param sb_const: Stefan-Boltzmann constant [4.903E-9 MJ K^-4 m^-2 day^-1]
    :param Tmin: minimum temperature for the given time period [C]
    :param Tmax: maximum temperature for the given time period [C]
    :return: net outgoing longwave radiaton [MJ m^-2 given_time_period^-1]
    """

    R_nl = sb_const*(((Tmin**4)+(Tmax**4))/2)*(0.34-(0.14*(math.sqrt(e_a))))*(1.35*(R_s/R_so)-0.35)

    return R_nl


def net_radiation(R_ns, R_nl):
    """
    The net radiation is the difference between the incoming shortwave radiaition and the outgoing longwave radiation.

    :param R_ns: net solar shortwave radiation [MJ m^-2 given_time_period^-1]
    :param R_nl: net outgoing longwave radiaton [MJ m^-2 given_time_period^-1]
    :return: net radiation [MJ m^-2 given_time_period^-1]
    """

    R_n = R_ns - R_nl

    return R_n


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
    time_now = datetime.now()  # Server in UTC so subtract 5 hrs for Lubbock TX

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
    C = (math.radians(1.9148) * math.sin(M)) + (math.radians(0.0200) * math.sin(2 * M)) + (
                math.radians(0.0003) * math.sin(3 * M))

    C = math.degrees(C)
    M = math.degrees(M)

    # Calculate the ecliptic longitude
    eclipt_long = (M + C + 180 + 102.9372) % 360

    # Calculate solar transit
    eclipt_long = math.radians(eclipt_long)
    M = math.radians(M)

    J_transit = J_yr_2000 + J_approx + (math.radians(0.0053) * math.sin(M)) - (
                math.radians(0.0069) * math.sin(2 * eclipt_long))

    # Calculate the declination of the sun.
    little_delta = math.asin((math.sin(eclipt_long) * math.sin(math.radians(23.44))))

    # Calculate the hour angle
    phi = latitude

    w_naught = math.acos((math.sin(math.radians(-0.83)) - (math.sin(math.radians(phi)) * math.sin(little_delta))) / (
                math.cos(math.radians(math.radians(phi))) * math.cos(little_delta)))

    # Calculate sunrise and sunset
    w_naught = math.degrees(w_naught)

    J_rise = J_transit - (w_naught / 360)
    J_set = J_transit + (w_naught / 360)

    sunrise = J_rise - 2451545.0
    sunset = J_set - 2451545.0

    todays_sunrise = (origin + timedelta(days=sunrise)) - timedelta(hours=UTC_offset)
    todays_sunset = (origin + timedelta(days=sunset)) - timedelta(hours=UTC_offset)

    return (todays_sunrise, todays_sunset)


def soil_heat_flux(R_n, sunrise, sunset):
    """
    For hourly or shorter time periods the soil heat flux (G) beneath a dense cover of grass (as one might observe in
    the hypothetical grass reference crop) does not correlate well with air temperature as is the case for daily mean
    values. G can be estimated for a given period with the following:

    Daytime: 0.1 * R_n
    Nighttime: 0.5 * R_n

    :param R_n: net radiation [MJ m^-2 given_time_period^-1]
    :return: soil heat flux for the given hourly or shorter period [MJ m^-2 given_time_period^-1]
    """

    current_time = datetime.now()

    if  sunrise < current_time < sunset:
        G = 0.1 * R_n

    else:
        G = 0.5 * R_n

    return  G


if __name__=="__main__":

    extraterrestrial_rad = et_solar_rad()
    solar_rad = solar_radiation(R_a=extraterrestrial_rad)
    clear_sky_rad = clear_sky_radiation(R_a=extraterrestrial_rad)
    net_shortwave_rad = net_shortwave_radiation(R_s=solar_rad)
    sat_vap_press = saturated_vap_pressure()
    act_vap_press = actual_vap_pressure(e_deg_T=sat_vap_press)
    net_longwave_rad = net_longwave_radiation(e_a=act_vap_press, R_s=solar_rad, R_so=clear_sky_rad)
    net_rad = net_radiation(R_ns=net_shortwave_rad, R_nl=net_longwave_rad)
    todays_sunrise, todays_sunset = sun_rise_set(latitude=33.576698, longitude=-101.855072, UTC_offset=5)
    soil_ht_flux = soil_heat_flux(R_n=net_rad, sunrise=todays_sunrise, sunset=todays_sunset)

    print(net_rad, soil_ht_flux)

