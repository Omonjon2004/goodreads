# Generated by Django 5.0.7 on 2024-07-25 15:33

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=128)),
                ('published', models.DateField()),
                ('isbn', models.CharField(max_length=128, unique=True)),
                ('language', models.CharField(blank=True, max_length=12, null=True)),
                ('page', models.IntegerField()),
                ('cover', models.ImageField(upload_to='book_cover/')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=28)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='avatar',
            field=models.ImageField(upload_to='avatar/'),
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('like_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviws', to='book.book')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bookshelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('books', models.ManyToManyField(related_name='shelfs', to='book.book')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelfs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='books', to='book.genre'),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('website', models.URLField(blank=True, max_length=128, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(upload_to='author_avatar/')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.genre')),
            ],
        ),
    ]