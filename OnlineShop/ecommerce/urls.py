from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
   

    path('registration/', registration_view, name='registration'),
    path('authorization/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),

    path('', base_view, name='base')
]
