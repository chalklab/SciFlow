# Generated by Django 4.1.4 on 2022-12-07 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Targdescs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=500)),
                ('source', models.CharField(blank=True, max_length=16, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'targdescs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Targids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=750)),
                ('source', models.CharField(blank=True, max_length=16, null=True)),
                ('comment', models.CharField(blank=True, max_length=128, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'targids',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Targsrcs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=32)),
                ('result', models.CharField(max_length=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'targsrcs',
                'managed': False,
            },
        ),
    ]