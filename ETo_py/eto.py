import math
from datetime import datetime, timedelta


class EToEstimator:
    """
    A class designed to generate an estimate of reference evapotranspiration as described by the FAO-56 ETo model.
    Details relating to FAO-56: http://www.fao.org/3/X0490E/X0490E00.htm
    """

    def __init__(self, **kwargs):
        self.latitude = kwargs['latitude']
        self.longitude = kwargs['longitude']
        self.air_temp = kwargs['air_temp']
        self.air_temp_min = kwargs['air_temp_min']
        self.air_temp_max = kwargs['air_temp_max']
        self.wind_speed = kwargs['wind_speed']  # meters per second
        self.relative_humidity = kwargs['relative_humidity']
        self.pressure = kwargs['pressure']
        self.period_length = kwargs['period_length']  # in minutes
        self.utc_offset = kwargs['utc_offset']
        self.time_now = None
        self.clock_at_midpoint = None
        self.clock_at_beginning = None
        self.clock_at_end = None
        self.todays_sunrise = None
        self.todays_sunset = None
        self.sbconst = 5.678E-8  # J s^-1 m^-2 K^-4
        self.r_a = None
        self.r_s = None
        self.r_so = None
        self.r_ns = None
        self.e_deg_t = None
        self.d = None
        self.e_a = None
        self.y = None
        self.r_n = None
        self.g = None
        self.eto = None
        self.print_switch = False

    def get_midpoint_period(self):
        """
        This function will grab the current time and return a midpoint for a given period in terms of hours as a float.
        If the period length is thirty minutes and the current time is 12:04 then the function will return 12.25 which
        is equal to 12:15 or the midpoint of a thirty minute period from 12:00 to 12:30. This value is necessary to
        estimate solar radiation for the given period length.

        :return: midpoint in terms of hours as float (0-24)
        """

        if isinstance(self.time_now, int):
            self.time_now = datetime.fromtimestamp(self.time_now)

        if not self.time_now:
            self.time_now = datetime.now()-timedelta(hours=self.utc_offset)
            self.time_now = self.time_now.timetuple()

        if self.time_now.tm_min < self.period_length:
            clock_at_midpoint = self.time_now.tm_hour + 0.25
            clock_at_beginning = self.time_now.tm_hour
            clock_at_end = self.time_now.tm_hour + 0.5

        else:
            clock_at_midpoint = self.time_now.tm_hour + .75
            clock_at_beginning = self.time_now.tm_hour + 0.5
            clock_at_end = self.time_now.tm_hour + 1

        self.clock_at_midpoint = clock_at_midpoint
        self.clock_at_beginning = clock_at_beginning
        self.clock_at_end = clock_at_end

        if self.print_switch:
            print('[INFO] Period beginning: {0}'.format(self.clock_at_beginning))
            print('[INFO] Period midpoint: {0}'.format(self.clock_at_midpoint))
            print('[INFO] Period end: {0}'.format(self.clock_at_end))

    def sun_rise_set(self):
        """ This is a function that will calculate sunrise and sunset from a given latitude and current time. The method
        for deriving sunrise and sunset from geolocation and Julian date was taken from the following Wikipedia page:

        https://en.wikipedia.org/wiki/Sunrise_equation

        :return: sunrise and sunset times
        """

        # The calculation below simply finds the difference between now and Jan 1, 2000 12:00 an adds leap seconds.
        j_yr_2000 = 2451545.0

        origin = datetime.strptime("2000-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
        time_now = datetime.now()  # Server in UTC so subtract 5 hrs for Lubbock TX

        # Difference between now and Jan 1, 2000 12:00.
        time_diff = time_now - origin

        n = time_diff.days

        # Calculate mean solar noon.
        l_w = self.longitude

        j_approx = n - (l_w / 360)

        # Calculate solar mean anomaly
        m = (357.5291 + 0.98560028 * j_approx) % 360

        m = math.radians(m)

        # Calculate the Equation of the center
        c = (math.radians(1.9148) * math.sin(m)) + (math.radians(0.0200) * math.sin(2 * m)) + (
                math.radians(0.0003) * math.sin(3 * m))

        c = math.degrees(c)
        m = math.degrees(m)

        # Calculate the ecliptic longitude
        eclipt_long = (m + c + 180 + 102.9372) % 360

        # Calculate solar transit
        eclipt_long = math.radians(eclipt_long)
        m = math.radians(m)

        j_transit = j_yr_2000 + j_approx + (math.radians(0.0053) * math.sin(m)) - (
                math.radians(0.0069) * math.sin(2 * eclipt_long))

        # Calculate the declination of the sun.
        little_delta = math.asin((math.sin(eclipt_long) * math.sin(math.radians(23.44))))

        # Calculate the hour angle
        phi = self.latitude

        w_naught = math.acos(
            (math.sin(math.radians(-0.83)) - (math.sin(math.radians(phi)) * math.sin(little_delta))) / (
                    math.cos(math.radians(math.radians(phi))) * math.cos(little_delta)))

        # Calculate sunrise and sunset
        w_naught = math.degrees(w_naught)

        j_rise = j_transit - (w_naught / 360)
        j_set = j_transit + (w_naught / 360)

        sunrise = j_rise - 2451545.0
        sunset = j_set - 2451545.0

        todays_sunrise = (origin + timedelta(days=sunrise)) - timedelta(hours=self.utc_offset)
        todays_sunset = (origin + timedelta(days=sunset)) - timedelta(hours=self.utc_offset)

        self.todays_sunrise = todays_sunrise
        self.todays_sunset = todays_sunset

        if self.print_switch:
            print('[INFO] Today\'s Sunrise: {0}'.format(self.todays_sunrise))
            print('[INFO] Today\'s Sunset: {0}'.format(self.todays_sunset))

    def et_solar_rad(self, latitude=33.576698, day_of_year=None):
        """
        Estimate extraterrestrial solar radiation. Extraterrestrial radiation is the radiation that strikes a plane
        perpendicular to the Sun's rays at the top of the Earth's atmosphere. This is the major energy source driving
        evapotranspiraton.

        :param latitude: latitude for location where [decimal degrees]
        :param day_of_year: day of year [integer]
        :return: extraterrestrial radiation for the given period [MJ m^-2 hour^-1]
        """

        # Calculate inverse relative distance Earth-Sun
        j = math.radians(latitude)
        d_r = 1 + 0.033 * math.cos(((2 * math.pi) / 365) * j)

        # Calculate solar declination
        little_delta = 0.409 * math.sin((((2 * math.pi) / 365) * j) - 1.39)

        # Seasonal correction for solar time
        if not day_of_year:
            day_of_year = datetime.now().timetuple().tm_yday

        b = ((2 * math.pi) * (day_of_year - 81)) / 364
        s_c = 0.1645 * math.sin(2 * b) - 0.1255 * math.cos(b) - 0.025 * math.sin(b)

        t = self.clock_at_midpoint

        # Solar time angle at midpoint of period
        l_z = -97.138451
        l_m = -101.855072
        little_omega = (math.pi / 12) * (t + (0.06667 * (l_z - l_m) + s_c) - 12)

        # Solar time angle at the beginning and end of the period
        t_1 = 0.5  # This is the length of the calculation period 1 for hour 0.5 for thirty minutes
        little_omega_1 = little_omega - ((math.pi * t_1) / 24)
        little_omega_2 = little_omega + ((math.pi * t_1) / 24)

        # Extraterrestrial radiation for hourly or shorter period
        g_sc = 0.0820  # MJ * m^-2 * min^-1
        r_a = ((12 * 60) / math.pi) * g_sc * d_r * (
                    (little_omega_2 - little_omega_1) * (math.sin(j) * math.sin(little_delta)) + (
                        math.cos(j) * math.cos(little_delta) * (math.sin(little_omega_2) - math.sin(little_omega_1))))

        self.r_a = r_a

        if self.print_switch:
            print('[INFO] Period extraterrestrial radiation: {0}'.format(self.r_a))

    def solar_radiation(self, n=1, max_n=1, a_s=0.25, b_s=0.5):
        """
        The portion of the extraterrestrial radiation that penetrates the atmosphere is denoted as R_s. The
        relationship between R_a and R_s can be expressed with the Angstrom formula: R_s = (a_s + b_s(n/N)) * R_a.
        Because this function is built for sub-day time spans relative sunshine duration (n/N) is set to one.

        The default values for the amount of R_a that reach Earth on overcast and clear-sky days has been set to a
        default of 0.25 and 0.5 respectively as per FAO-56 recommendation. These parameters can me adjusted based
        on local experimental data however.

        :param n: actual duration of sunshine [hour as float]
        :param max_n: max possible duration of sunshine [hour as float]
        :param a_s: regression constant, the fraction of R_a that reaches Earth on overcast day (n=0)
        :param b_s: fraction of R_a that reaches Earth on clear days (n=N)
        :return: solar radiation (R_s) [MJ m^-2 given_time_period^-1]
        """

        r_s = (a_s + (b_s * (n / max_n))) * self.r_a

        self.r_s = r_s

        if self.print_switch:
            print('[INFO] Period incoming solar radiation: {0}'.format(self.r_s))

    def clear_sky_radiation(self, a_s=0.75, b_s=2E-5, z=976):
        """
        The calculation of clear-sky radiation is requisite in the estimation of net longwave radiation. This
        calculation requires a_s and b_s which can be calibrated through experimentation.

        In cases where calibration data are not available a value of 0.75 can be used for a_s and 2E-5 for b_s.

        :param a_s: regression constant, the fraction of R_a that reaches Earth on overcast day (n=0)
        :param b_s: fraction of R_a that reaches Earth on clear days (n=N)
        :param z: location elevation in meters, 976 for Lubbock, TX
        :return: clear-sky radiation (R_so) [MJ m^2 given_time_period^-1]
        """

        r_so = (a_s + (b_s * z)) * self.r_a

        self.r_so = r_so

        if self.print_switch:
            print('[INFO] Period clear-sky radiation: {0}'.format(self.r_so))

    def net_shortwave_radiation(self, albedo=0.23):
        """
        Net shortwave radiation (R_ns) results from the balance between incoming and reflected solar radiation as
        described by: R_ns = (1-albedo) * R_s

        :param albedo: canopy reflection for the hypothetical reference crop [dimensionless]
        :return: net solar shortwave radiation [MJ m^-2 given_time_period^-1]
        """

        r_ns = (1 - albedo) * self.r_s

        self.r_ns = r_ns

        if self.print_switch:
            print('[INFO] Period net shortwave radiation: {0}'.format(self.r_ns))

    def saturated_vap_pressure(self):
        """
        A calculation a saturation vapor pressure based on air temperature as expressed by:
        e_deg_T = 0.6108 e ((17.27 * T) / (T + 237.3))

        :return: saturation vapor pressure at the given temperature [kPa]
        """

        e_deg_t = 0.6018 * math.exp((17.27 * self.air_temp) / (self.air_temp + 237.3))

        self.e_deg_t = e_deg_t

        if self.print_switch:
            print('[INFO] Period saturated vapor pressure: {0}'.format(self.e_deg_t))

    def slope_sat_vap_pressure(self):
        """
        The relationship between saturation vapor pressure and temperature (D) is required in the calculation
        of evapotranspiration. The slope of this curve is given by: D = (4098 * e_deg_T) / (T + 237.3)

        :return: slope of saturation vapor pressure curve at air temperature T [kPa C^-1]
        """

        d = (4098 * self.e_deg_t) / ((self.air_temp + 237.3) ** 2)

        self.d = d

        if self.print_switch:
            print('[INFO] Period slope for saturated vapor pressure: {0}'.format(self.d))

    def actual_vap_pressure(self):
        """
        A calculation of actual vapor pressure based on current saturation vapor pressure and relative humidity.

        :return: actual vapor pressure at the given RH [kPa]
        """

        e_a = self.e_deg_t * self.relative_humidity

        self.e_a = e_a

        if self.print_switch:
            print('[INFO] Period actual vapor pressure: {0}'.format(self.e_a))

    def psychrometric_constant(self, c_p=1.1013E-3, latent_heat=2.45, e_ratio=0.622):
        """
        The psychrometric constant relates the partial pressure of water in the air to the air temperature.

        :param c_p: specific heat at a constant pressure [MJ kg^-1 C^-1]
        :param latent_heat: the latent heat of vaporization, 2.45 [MJ kg^-1]
        :param e_ratio: the ratio of molecular weight of water vapor to dry air = 0.622
        :return: psychrometric constant [kPa C^-1]

        The specific heat at constant pressure is the amount of energy required to increase the temperature of a unit
        mass of air by one degree at constant pressure. This value depends on the composition of the air, i.e, on
        humidity.
        """

        y = (c_p * self.pressure) / (e_ratio * latent_heat)

        self.y = y

        if self.print_switch:
            print('[INFO] Psychrometric constant at current temperature: {0}'.format(self.y))

    def net_longwave_radiation(self):
        """
        The outgoing net longwave radiation must be calculated to estimate the radiation energy balance. The rate of
        longwave emission is proportional to the absolute temperature of the surfaces raised to the fourth power. The
        actual amount of longwave radiation leaving the Earth is less than that given by the Stefan-Boltzman law due
        to the absorption and downward radiation of the sky. Water vapor, clouds, carbon dioxide, and dust are absorbers
        and emitters of longwave radiation. Their concentrations can be known when estimation outgoing longwave flux.
        As humidiy and cloudiness play an important role, the Stefan-Boltzmann law is corrected by these two factors
        when estimating outgoing longwave radiation. The concentrations of the other absorbers are assumed to remain
        constant.

        This estimation takes the following form:

        R_nl = sb_const * ((Tmax_K**4 + Tmin_K**4)/2) * (0.34-0.14*(e_a**(1/2))) * (1.35 * (R_s / R_so) - 0.35)

        :return: net outgoing long wave radiation [MJ m^-2 given_time_period^-1]
        """

        # convert to megajoules and evaluate for the given time period in seconds
        time_period_seconds = self.period_length * 60
        sbc = self.sbconst * .0001 * time_period_seconds

        r_n = sbc * (((self.air_temp_min ** 4) + (self.air_temp_max ** 4)) / 2) * \
            (0.34 - (0.14 * (math.sqrt(self.e_a)))) * (1.35 * (self.r_s / self.r_so) - 0.35)

        self.r_n = r_n

        if self.print_switch:
            print('[INFO] Period net longwave radiation: {0}'.format(self.r_n))

    def soil_heat_flux(self):
        """
        For hourly or shorter time periods the soil heat flux (G) beneath a dense cover of grass (as one might observe
        in the hypothetical grass reference crop) does not correlate well with air temperature as is the case for daily
        mean values.

        G can be estimated for a given period with the following:

        Daytime: 0.1 * R_n
        Nighttime: 0.5 * R_n

        :return: soil heat flux for the given hourly or shorter period [MJ m^-2 given_time_period^-1]
        """

        current_time = datetime.now()

        if self.todays_sunrise < current_time < self.todays_sunset:
            g = 0.1 * self.r_n

        else:
            g = 0.5 * self.r_n

        self.g = g

        if self.print_switch:
            print('[INFO] Period soil heat flux: {0}'.format(self.g))

    def estimate_eto(self):
        """
        In areas where there are significant intra-day changes in wind speed, dewpoint or cloudiness, it is beneficial
        to calculate ETo at a sub day time span, therefore enhancing the ETo estimate.

        The equation takes the following form:

        eto = (0.408 * D * (R_n - G))+(y * (37 / (T_period + 237)) * U_2 * (e_deg_T - e_a)))/(D + y * (1 + 0.34 * u_2))

        :return:
        """

        self.get_midpoint_period()
        self.sun_rise_set()
        self.et_solar_rad()
        self.solar_radiation()
        self.clear_sky_radiation()
        self.net_shortwave_radiation()
        self.saturated_vap_pressure()
        self.slope_sat_vap_pressure()
        self.actual_vap_pressure()
        self.psychrometric_constant()
        self.net_longwave_radiation()
        self.soil_heat_flux()

        numerator = (0.408 * self.d * (self.r_n - self.g)) + (self.y * (37 / (self.period_length + 273))) * \
                    (self.wind_speed * (self.e_deg_t - self.e_a))

        denominator = (self.d + (self.y * (1 + 0.34 * self.wind_speed)))

        eto = numerator / denominator

        self.eto = eto

        if self.print_switch:
            print('[INFO] Estimated ETo: {0}'.format(self.eto))


if __name__ == "__main__":

    current_obs = {
        'latitude': 33.576698,
        'longitude': -101.855072,
        'air_temp': 33,
        'air_temp_min': 33,
        'air_temp_max': 33,
        'wind_speed': 5.5,
        'relative_humidity': .42,
        'period_length': 30,
        'pressure': 101.6,
        'utc_offset': 5,
        'print_switch': True,
    }

    eto_estimate = EToEstimator(**current_obs)
    eto_estimate.estimate_eto()

    print(eto_estimate.eto*24)
