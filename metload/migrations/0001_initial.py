# Generated by Django 2.1.7 on 2019-04-03 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Obsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality_message', models.CharField(blank=True, max_length=80, null=True)),
                ('datetime', models.IntegerField(blank=True, null=True)),
                ('cod', models.CharField(blank=True, max_length=50, null=True)),
                ('city_count', models.CharField(blank=True, max_length=20, null=True)),
                ('site_id', models.CharField(blank=True, max_length=20, null=True)),
                ('site_name', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('pressure', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('humidity', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('wind_speed', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('wind_dir', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('wind_gust', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('rain_1h', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('rain_3h', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('snow', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('weather_id', models.IntegerField(blank=True, null=True)),
                ('weather_main', models.CharField(blank=True, max_length=20, null=True)),
                ('weather_desc', models.CharField(blank=True, max_length=20, null=True)),
                ('weather_icon', models.CharField(blank=True, max_length=20, null=True)),
                ('st_clouds', models.CharField(blank=True, max_length=20, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='locations.Location')),
            ],
        ),
    ]
