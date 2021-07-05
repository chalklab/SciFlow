# Generated by Django 3.1.2 on 2020-10-09 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AspectActlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aspect_lookup_id', models.IntegerField()),
                ('aspect_file_id', models.IntegerField()),
                ('activitycode', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=256)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'aspect_actlog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AspectErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aspect_lookup_id', models.IntegerField()),
                ('aspect_file_id', models.IntegerField()),
                ('errorcode', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=256)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'aspect_errors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AspectFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aspect_lookup_id', models.IntegerField()),
                ('file', models.TextField()),
                ('type', models.CharField(max_length=32)),
                ('version', models.IntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'aspect_files',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AspectLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueid', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=16)),
                ('graphname', models.CharField(max_length=256)),
                ('currentversion', models.IntegerField()),
                ('auth_user_id', models.PositiveIntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'aspect_lookup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FacetActlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facet_lookup_id', models.IntegerField()),
                ('facet_file_id', models.IntegerField()),
                ('activitycode', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=256)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'facet_actlog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FacetErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facet_lookup_id', models.IntegerField()),
                ('facet_file_id', models.IntegerField()),
                ('errorcode', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=256)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'facet_errors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FacetFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facet_lookup_id', models.IntegerField()),
                ('file', models.TextField()),
                ('type', models.CharField(max_length=32)),
                ('version', models.IntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'facet_files',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FacetLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueid', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=16)),
                ('graphname', models.CharField(max_length=256)),
                ('currentversion', models.IntegerField()),
                ('auth_user_id', models.PositiveIntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'facet_lookup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JsonActlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=24)),
                ('json_lookup_id', models.IntegerField()),
                ('json_file_id', models.IntegerField()),
                ('activitycode', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=256)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'json_actlog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JsonErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=24)),
                ('json_lookup_id', models.IntegerField()),
                ('json_file_id', models.IntegerField()),
                ('errorcode', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=256)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'json_errors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JsonFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_lookup_id', models.IntegerField()),
                ('file', models.TextField()),
                ('type', models.CharField(max_length=32)),
                ('version', models.IntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'json_files',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JsonLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset_id', models.IntegerField()),
                ('uniqueid', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=256)),
                ('graphname', models.CharField(max_length=256)),
                ('currentversion', models.IntegerField()),
                ('auth_user_id', models.PositiveIntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'json_lookup',
                'managed': False,
            },
        ),
    ]
