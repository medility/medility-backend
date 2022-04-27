# Generated by Django 3.2.7 on 2021-09-29 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeslot', '0004_auto_20210929_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurseSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SlotDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_date', models.DateField()),
                ('slot', models.ManyToManyField(through='timeslot.NurseSlot', to='timeslot.TimeSlot')),
            ],
        ),
        migrations.AddField(
            model_name='nurseslot',
            name='date_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeslot.slotdate'),
        ),
        migrations.AddField(
            model_name='nurseslot',
            name='nurse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nurseslot',
            name='time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeslot.timeslot'),
        ),
    ]
