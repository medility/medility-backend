# Generated by Django 3.2.7 on 2022-01-28 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comunity', '0007_auto_20220128_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitygroup',
            name='communityUser',
        ),
        migrations.CreateModel(
            name='CommunityGroupInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('communityGroupInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comunity.communitygroup')),
                ('communityUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comunity.communityuserinfo')),
            ],
        ),
    ]
