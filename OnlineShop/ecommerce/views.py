from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import CreateView
from ecommerce.models import *
from decimal import Decimal
from django.core.paginator import Paginator
from .forms import *
from django.core.mail import send_mail


def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all()
    products = Product.objects.all().order_by('-date_added')[0: 8]
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }
    return render(request, 'index.html', context)


def category_view(request, category_slug, page=1):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    ordering = request.GET.get('ordering')
    if ordering == None:
        ordering = 'price'

    category = Category.objects.get(slug=category_slug)

    if ordering == 'title':
        category_products_list = Product.objects.filter(
            category=category).order_by('brand', 'title')
    else:
        category_products_list = Product.objects.filter(
            category=category).order_by(ordering)

    categories = Category.objects.all()

    paginator = Paginator(category_products_list, 8)

    page = request.GET.get('page')
    category_products = paginator.get_page(page)

    context = {
        'category': category,
        'category_products': category_products,
        'categories': categories,
        'cart': cart,
        'ordering': ordering,
    }
    return render(request, 'category.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']

        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        return HttpResponseRedirect(reverse('base'))
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form
    }
    return render(request, 'registration.html', context)

