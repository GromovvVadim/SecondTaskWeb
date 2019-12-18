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


class CartItem(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, verbose_name='Book')
    amount = models.PositiveIntegerField(default=1, verbose_name='Count')
    total_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return 'CartItem ({0})'.format(self.product.title)


class Cart(models.Model):
    items = models.ManyToManyField(
        'CartItem', blank=True, verbose_name='Books')
    total_price = models.DecimalField(blank=True, default=0,
                                      max_digits=9, decimal_places=2, verbose_name='Price')

    def add_to_cart(self, product_slug):
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(
            product=product, total_price=product.price)
        if new_item not in self.items.all():
            self.items.add(new_item)
            self.save()

    def remove_from_cart(self, product_slug):
        product = Product.objects.get(slug=product_slug)
        for cart_item in self.items.all():
            if cart_item.product == product:
                self.items.filter(product=product).delete()
                self.save()

    def change_item_amount(self, item_id, amount):
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.amount = int(amount)
        cart_item.total_price = int(amount) * float(cart_item.product.price)
        cart_item.save()

        total_sum = 0.00
        for item in self.items.all():
            total_sum += float(item.total_price)
        self.total_price = total_sum
        self.save()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Baskets'
        verbose_name = 'Basket'


ORDER_STATUSES = (
    ('Processing', 'Processing'),
    ('Paid', 'Paid'),
    ('Rejected', 'Rejected')
)

DELIVERY_TYPES = (
    ('Pickup by myself', 'Pickup by myself'),
    ('Delivery', 'Delivery')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.CASCADE, verbose_name="Customer")
    name = models.CharField(max_length=200, verbose_name="First Name")
    surname = models.CharField(max_length=200, verbose_name="Second Name")
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    address = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Address")
    items = models.ForeignKey(
        Cart, on_delete=models.PROTECT, verbose_name="Books", null=True)
    total_price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00, verbose_name='Price')
    delivery_type = models.CharField(
        max_length=100, choices=DELIVERY_TYPES, default='Pickup by myself')
    comment = models.TextField(null=True, blank=True, verbose_name="Comment")
    date = models.DateTimeField(
        auto_now_add=True, auto_now=False, verbose_name="Date")
    status = models.CharField(
        max_length=100, choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0])

    def __str__(self):
        return 'Order № ' + str(self.id)


class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач")
    comment = models.TextField(verbose_name='Comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Book')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')