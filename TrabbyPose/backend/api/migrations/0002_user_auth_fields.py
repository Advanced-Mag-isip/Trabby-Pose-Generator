# Generated migration for adding is_admin field and updating User model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_address',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_permitted',
            field=models.IntegerField(default=1),
        ),
        # migrations.AddField(
        #     model_name='user',
        #     name='__str__',
        #     field=None,
        # ),
    ]
