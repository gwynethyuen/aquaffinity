# Generated by Django 3.1.5 on 2021-02-05 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Your Post Title', max_length=60)),
                ('body', models.TextField(default='Your Post Text')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.CharField(default='John Doe', max_length=1000)),
                ('category', models.CharField(choices=[(1, 'Announcements'), (2, 'Team Events'), (3, 'Academics'), (4, 'Swim/Dive'), (5, 'Misc')], default=5, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Swimmer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='John Doe', max_length=50)),
                ('hometown', models.CharField(default='Troy, NY', max_length=50)),
                ('class_year', models.CharField(default='FR', max_length=2)),
                ('event_list', models.TextField(default='There are no recent events.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=60)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.post')),
            ],
        ),
    ]
