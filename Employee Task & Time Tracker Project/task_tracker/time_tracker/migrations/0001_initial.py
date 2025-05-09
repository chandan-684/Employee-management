# Generated by Django 5.1.5 on 2025-04-24 11:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='JobRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='AnnualLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Granted'), (3, 'Rejected'), (4, 'Cancelled')], verbose_name='status')),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
                ('comments', models.TextField(blank=True, max_length=500, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_employee', to=settings.AUTH_USER_MODEL)),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_recorded_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='time_tracker.department')),
                ('line_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_line_manager', to=settings.AUTH_USER_MODEL)),
                ('job_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='time_tracker.jobrole')),
            ],
        ),
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_datetime', models.DateTimeField(auto_now_add=True)),
                ('clocking_time', models.DateTimeField()),
                ('logging', models.CharField(choices=[('IN', 'In'), ('OUT', 'Out')], max_length=3)),
                ('ip_address', models.GenericIPAddressField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_employee', to=settings.AUTH_USER_MODEL)),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_recorded_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'clocking_time',
            },
        ),
    ]
