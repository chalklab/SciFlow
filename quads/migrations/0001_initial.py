# Generated by Django 4.0.5 on 2022-06-16 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.CharField(max_length=256)),
                ('prd', models.CharField(max_length=256)),
                ('obj', models.CharField(max_length=256)),
                ('gph', models.CharField(max_length=256)),
                ('tmp', models.CharField(max_length=32)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'quads',
                'managed': False,
            },
        ),
    ]
