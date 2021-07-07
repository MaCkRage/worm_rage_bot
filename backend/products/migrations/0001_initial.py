# Generated by Django 3.2.5 on 2021-07-07 22:14

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Название категории')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': '(Под)Категория',
                'verbose_name_plural': 'Категорий (дерево)',
                'ordering': ('title',),
                'default_related_name': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='public/media/%Y/%M/%D', verbose_name='Фотография товара')),
                ('rating_average', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Средний рейтинг')),
                ('rating_count', models.IntegerField(blank=True, null=True, verbose_name='Кол-во отзывов')),
                ('date_first_available', models.DateTimeField(blank=True, null=True, verbose_name='Доступно к покупке с')),
                ('product_link', models.CharField(blank=True, max_length=240, null=True, verbose_name='Ссылка')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_category', to='products.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'default_related_name': 'products',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_prices', to='products.product', verbose_name='Товар')),
                ('seller', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sellers_prices', to='user.seller', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
                'default_related_name': 'prices',
            },
        ),
    ]