# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Product, Brand, Category


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Login"
        self.fields['username'].help_text = ""
        self.fields['password'].label = 'Password'
        self.fields['password_check'].label = 'Repeat password'
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = 'Second Name'
        self.fields['email'].label = 'E-mail'

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                {'username': 'This login is already registered'}, code='user exists')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                {'email': 'Such mail is already registered'}, code='email exists')
        if password != password_check:
            raise forms.ValidationError(
                {'password_check': 'Passwords do not match'}, code='passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                {'username': 'There is no such login'}, code='user does not exist')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError(
                {'password': 'The password is incorrect'}, code='password does not exist')

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



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'category', 'brand', 'slug', 'description',
                  'price', 'image', 'is_available']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['name']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'slug']


class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач")
    comment = models.TextField(verbose_name='Comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Book')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')