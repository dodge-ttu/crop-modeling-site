from django.db import models
from locations.models import Location

class Obsset(models.Model):
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    quality_message = models.CharField(max_length=80, blank=True, null=True)
    datetime = models.IntegerField(blank=True, null=True)
    cod = models.CharField(max_length=50, blank=True, null=True)
    city_count = models.CharField(max_length=20, blank=True, null=True)
    site_id = models.CharField(max_length=20, blank=True, null=True)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    sunrise = models.IntegerField(blank=True, null=True)
    sunset = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    humidity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temp_min = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temp_max = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    wind_dir = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    wind_gust = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rain_1h = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rain_3h = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    snow = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    weather_id = models.IntegerField(blank=True, null=True)
    weather_main = models.CharField(max_length=20, blank=True, null=True)
    weather_desc = models.CharField(max_length=20, blank=True, null=True)
    weather_icon = models.CharField(max_length=20, blank=True, null=True)
    st_clouds = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.site_name
