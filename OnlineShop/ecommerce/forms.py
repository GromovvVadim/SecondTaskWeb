# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Product, Brand, Order, Category, ProductComment


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


class OrderForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    phone = forms.CharField()
    delivery_type = forms.ChoiceField(widget=forms.Select(), choices=(
        [("self", "Pickup by myself"), ("delivery", "Delivery")]))
    date = forms.DateField(
        widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "First Name"
        self.fields['surname'].label = 'Second Name'
        self.fields['phone'].label = 'Phone number'
        self.fields['phone'].help_text = "Input real number"
        self.fields['delivery_type'].label = 'The method of obtaining'
        self.fields['address'].label = 'Delivery address'
        self.fields['comment'].label = 'Order comment'
        self.fields['date'].label = 'Delivery date'
        self.fields['date'].help_text = 'Delivery takes 2-4 days'


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


class CommentForm(forms.ModelForm):

    class Meta:
        model = ProductComment
        fields = ['comment']
