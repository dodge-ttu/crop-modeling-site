# In areas where there are significant intra-day changes in wind speed, dewpoint or cloudiness, it is beneficial to
# calculate ETo at a sub day time span, therefore enhancing the ETo estimate.
#
# The equation takes the following form:
#
# eto = (0.408 * D * (R_n - G)) + (y * (37 / (T_period + 237)) * U_2 * (e_deg_T - e_a))) / (D + y * (1 + 0.34 * u_2))
#
# eto: reference evapotranspiration [mm given_time_period^-1]
# R_n: net radiation at the grass surface [MJ m^-2 hour^-1]
# G: soil heat flux density [MJ m^-2 hour^-1]
# T_period: mean temperature for the given time period [C]
# D: saturation slope vapor pressure curve at T_period [kPa C^-1]
# y: psychrometric constant [kPa C^-1]
# e_deg_T: saturation vapor pressure at air temperature T_period [kPa]
# e_a: average actual vapor pressure for the given time period [kPa]
# u_2: average wind speed for the given time period

from ETo_py import solar_rad_per_unit_time as sol_rad
from ETo_py import sunrise_sunset as ss

def estimate_eto(R_n, G, T_period, D, y, e_deg_T, e_a, u_2):

    numerator = (0.408*D*(R_n-G)) + (y*(37/(T_period+273)))*(u_2*(e_deg_T-e_a))
    denominator = (D+(y*(1+0.34*u_2)))

    eto = numerator / denominator

    return  eto


if __name__=="__main__":

    import matplotlib.pyplot as plt

    eto_values = []
    temp_values = list(range(100))
    for temp in temp_values:
        extraterrestrial_rad = sol_rad.et_solar_rad(latitude=33.576698, day_of_year=1)
        solar_rad = sol_rad.solar_radiation(R_a=extraterrestrial_rad)
        clear_sky_rad = sol_rad.clear_sky_radiation(R_a=extraterrestrial_rad)
        net_shortwave_rad = sol_rad.net_shortwave_radiation(R_s=solar_rad)
        sat_vap_press = sol_rad.saturated_vap_pressure(air_temp=temp)
        act_vap_press = sol_rad.actual_vap_pressure(e_deg_T=sat_vap_press, relative_humidity=.30)
        slope_sat_vap = sol_rad.slope_sat_vap_pressure(e_deg_T=sat_vap_press, T_period=temp)
        psychro_const = sol_rad.psychrometric_constant(pressure=101.8, c_p=1.1013E-3, latent_heat=2.45, e_ratio=0.622)
        net_longwave_rad = sol_rad.net_longwave_radiation(e_a=act_vap_press, R_s=solar_rad, R_so=clear_sky_rad, Tmin=temp, Tmax=temp)
        net_rad = sol_rad.net_radiation(R_ns=net_shortwave_rad, R_nl=net_longwave_rad)
        todays_sunrise, todays_sunset = ss.sun_rise_set(latitude=33.576698, longitude=-101.855072, UTC_offset=5)
        soil_ht_flux = sol_rad.soil_heat_flux(R_n=net_rad, sunrise=todays_sunrise, sunset=todays_sunset)
        avg_wind_speed = 0  # meters per second

        params = {
            "R_n": net_rad,
            "G": soil_ht_flux,
            "T_period": temp,
            "D": slope_sat_vap,
            "y": psychro_const,
            "e_deg_T": slope_sat_vap,
            "e_a": act_vap_press,
            "u_2": avg_wind_speed,
        }

        eto = estimate_eto(**params)
        eto_values.append(eto)


    x = temp_values
    y = eto_values

    fig, axs = plt.subplots(1,1, figsize=(10,10))
    axs.plot(x,y)
    fig.savefig("/home/will/crop_mod_site/ETo_py/eto_vs_temp.pdf")
