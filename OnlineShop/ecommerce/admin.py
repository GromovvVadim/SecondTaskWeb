from django.contrib import admin

from ecommerce.models import *

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductComment)
admin.site.register(Cart)
admin.site.register(CartItem)