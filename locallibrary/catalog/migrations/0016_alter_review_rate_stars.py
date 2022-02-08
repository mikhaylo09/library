# Generated by Django 4.0.1 on 2022-02-08 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_review_book_alter_review_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default='5', help_text='Rate book'),
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avgstar', models.IntegerField()),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.book', unique=True)),
            ],
        ),
    ]
