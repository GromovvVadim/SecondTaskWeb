from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        ordering = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Author')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'
        verbose_name = 'Author'
        ordering = ['name']


def get_image_folder(instance, file):
    file = instance.slug + '.' + file.split('.')[1]
    return '{0}/{1}'.format(instance.slug, file)


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Book')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Category')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Author')
    slug = models.SlugField(max_length=100)
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Price')
    image = models.ImageField(
        upload_to=get_image_folder, null=True, blank=False, verbose_name='Photo')
    is_available = models.BooleanField(
        default=True, blank=True, verbose_name='In stock')
    date_added = models.DateTimeField(
        auto_now_add=True, auto_now=False, verbose_name='Added', blank=True)

    def __str__(self):
        return str(self.brand) + ' ' + str(self.title)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"product_slug": self.slug})

    class Meta:
        verbose_name_plural = 'Books'
        verbose_name = 'Book'
        ordering = ['title']





