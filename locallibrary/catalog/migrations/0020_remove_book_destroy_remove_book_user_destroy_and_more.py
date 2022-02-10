# Generated by Django 4.0.1 on 2022-02-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_rename_userdestroy_book_user_destroy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='destroy',
        ),
        migrations.RemoveField(
            model_name='book',
            name='user_destroy',
        ),
        migrations.AddField(
            model_name='book',
            name='date_create',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='date_update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='state',
            field=models.IntegerField(blank=True, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.IntegerField(blank=True, null=True, verbose_name='Rating'),
        ),
    ]
