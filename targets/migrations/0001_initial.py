# Generated by Django 4.0.5 on 2022-06-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Targets',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('type', models.CharField(blank=True, max_length=32, null=True)),
                ('organism', models.CharField(blank=True, max_length=32, null=True)),
                ('tax_id', models.CharField(blank=True, max_length=8, null=True)),
                ('chembl_id', models.CharField(blank=True, max_length=16, null=True)),
                ('graphdb', models.CharField(blank=True, max_length=256, null=True)),
                ('comments', models.CharField(blank=True, max_length=256, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'targets',
                'managed': False,
            },
        ),
    ]