from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
   
    path('category/<str:category_slug>', category_view, name='category_detail'),
    path('registration/', registration_view, name='registration'),
    path('authorization/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('change_item_amount/', change_item_amount, name="change_item_amount"),
    path('add_comment/<str:product_slug>', add_comment, name='add_comment'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', create_order, name='create_order'),
    path('accept_order/', accept_order, name='accept_order'),
    path('', base_view, name='base')
]
