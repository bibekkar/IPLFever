# Generated by Django 2.0.3 on 2018-04-12 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='betting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('team', models.CharField(max_length=3)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='fixtures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(max_length=3)),
                ('team2', models.CharField(max_length=3)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=15)),
                ('venue', models.CharField(max_length=50)),
                ('result', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Usertable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10)),
                ('pwd', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='betting',
            name='match_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.fixtures'),
        ),
    ]
