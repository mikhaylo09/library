# Generated by Django 4.0.1 on 2022-02-06 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_rename_rate_review_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='book',
            new_name='title',
        ),
    ]