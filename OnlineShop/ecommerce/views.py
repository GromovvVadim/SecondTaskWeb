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


def product_view(request, product_slug):
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

    product = Product.objects.get(slug=product_slug)

    categories = Category.objects.all()
    comments = ProductComment.objects.filter(product=product)

    form = CommentForm()

    context = {
        'product': product,
        'comments': comments,
        'categories': categories,
        'cart': cart,
        'form': form
    }
    return render(request, 'product.html', context)


def cart_view(request):
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

    total_sum = Decimal()
    for item in cart.items.all():
        total_sum += Decimal(item.total_price)
    cart.total_price = total_sum

    context = {
        'cart': cart,
        'cart_total_price': cart.total_price,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
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

    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)

    total_sum = 0.00
    for item in cart.items.all():
        total_sum += float(item.total_price)
    cart.total_price = total_sum
    cart.save()

    return JsonResponse({
        'cart_total': cart.items.count(),
        'cart_total_price': cart.total_price,
    })


def remove_from_cart(request):
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

    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)

    total_sum = 0.00
    for item in cart.items.all():
        total_sum += float(item.total_price)
    cart.total_price = total_sum
    cart.save()

    return JsonResponse({
        'cart_total': cart.items.count(),
        'cart_total_price': cart.total_price,
    })


def change_item_amount(request):
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

    amount = request.GET.get('amount')
    item_id = request.GET.get('item_id')
    cart.change_item_amount(item_id, amount)
    cart_item = CartItem.objects.get(id=int(item_id))

    return JsonResponse({
        'cart_total': cart.items.count(),
        'item_total_price': cart_item.total_price,
        'cart_total_price': cart.total_price,
    })


def checkout_view(request):
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

    context = {
        'cart': cart
    }
    return render(request, 'checkout.html', context)


def create_order(request):
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

    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'order.html', context)


def accept_order(request):
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

    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        surname = form.cleaned_data['surname']
        phone = form.cleaned_data['phone']
        delivery_type = form.cleaned_data['delivery_type']
        address = form.cleaned_data['address']
        comment = form.cleaned_data['comment']

        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total_price=cart.total_price,
            name=name,
            surname=surname,
            phone=phone,
            address=address,
            delivery_type=delivery_type,
            comment=comment
        )

        del request.session['cart_id']
        del request.session['total']
    return render(request, 'thank_you.html', {})

def cabinet_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    context = {
        'orders': orders
    }
    return render(request, 'cabinet.html', context)


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

@login_required
def add_comment(request, product_slug):
    comment = request.POST.get('comment')
    product = Product.objects.get(slug=product_slug)
    new_comment = ProductComment()
    new_comment.user = request.user
    new_comment.comment = comment
    new_comment.product = product
    new_comment.save()

    comments = ProductComment.objects.filter(product=product)

    return HttpResponseRedirect(reverse('product_detail', kwargs={'product_slug': product_slug}))
