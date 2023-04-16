# Generated by Django 4.2 on 2023-04-16 15:38

from django.db import migrations, models
import image_app.storage_backends


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('image', models.ImageField(height_field='height', max_length=5120000, storage=image_app.storage_backends.PublicImagesStorage(), upload_to='', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, null=True)),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
    ]