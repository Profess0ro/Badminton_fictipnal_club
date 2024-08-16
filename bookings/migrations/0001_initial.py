# Generated by Django 4.2.13 on 2024-08-16 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('GR', 'Grass'), ('GV', 'Gravel')], max_length=2)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('court_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.courttype')),
            ],
        ),
    ]
