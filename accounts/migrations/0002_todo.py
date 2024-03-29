# Generated by Django 3.1.5 on 2021-03-28 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(default='NULL', max_length=100)),
                ('iscomplete', models.BooleanField(default=False)),
                ('student', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
