# Generated by Django 5.1.3 on 2025-01-02 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='url',
            field=models.URLField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
