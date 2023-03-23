from itertools import product
from statistics import quantiles
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})
        else:
            return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'qauntity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'qauntity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'REDMI' or data == 'SAMSUNG':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Asus' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__lt=10000)
    elif data == 'above':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'laptops': laptops})


def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='T')
    elif data == 'H&M' or data == 'Zara':
        topwears = Product.objects.filter(category='T').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(
            category='T').filter(discounted_price__lt=10000)
    elif data == 'above':
        topwears = Product.objects.filter(
            category='T').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'topwears': topwears})


def bottmowear(request, data=None):
    if data == None:
        bottmowears = Product.objects.filter(category='M')
    elif data == 'H&M' or data == 'Zara':
        bottmowears = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        bottmowears = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        bottmowears = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'bottmowears': bottmowears})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/cutomerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.succes(
                request, 'Congratulation!! Registered succesfully'
            )
            form.save()
        return render(request, 'app/cutomerregistration.html', {'form': form})


def buy_now(request):
    return render(request, 'app/buynow.html')





def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn_primary'})


def orders(request):
    return render(request, 'app/orders.html')


def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request):
    return render(request, 'app/mobile.html')


def login(request):
    return render(request, 'app/login.html')


def checkout(request):
    return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    
    def post(self, request):
       form = CustomerProfileForm(request.POST)
       if form.is_valid():
           user = request.user
           name = form.cleaned_data['name']
           locality = form.cleaned_data['locality']
           city = form.cleaned_data['city']
           state = form.cleaned_data['state']
           zipcode = form.cleaned_data['zipcode']
           reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
           reg.save()
           messages.success(request,'congratulation! Profile Updated Succesfully ')
       return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary`'})
        