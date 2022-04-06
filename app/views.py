from email import message
from itertools import product
from multiprocessing import context
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import redirect, render, redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,Comment
from .forms import CustomerRegistrationForm,CustomerProfileForm,CommentForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops})

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        num_comments= Comment.objects.filter(product_id=pk).count()
        # print(num)
        # num_comments = Comment.objects.all().count()
        return render(request,'app/productdetail.html',{'product':product,'num_comments':num_comments})

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount= 90.0
        total_amount = 0.0
        #list comprehension
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request, 'app/emptycart.html',)
        

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request,data=None):
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Apple' or data == 'Redmi' or data =='Samsung' or data =='Pixel' or data=='OnePlus' or data=='Realme' or data=='Vivo':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request,data=None):
    if data == None:
        laptops=Product.objects.filter(category='L')
    elif data=='MSI' or data == 'Asus' or data =='LG' or data =='HP' or data=='Mac' or data=='Lenovo' or data=='Razer':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptops=Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data=='above':
        laptops=Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    return render(request, 'app/laptop.html',{'laptops':laptops})

def bottomwear(request,data=None):
    if data == None:
        bottomwears=Product.objects.filter(category='BW')
    elif data=='BW-Collection' or data =='BlueMoon':
        bottomwears=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
    elif data=='above':
        bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})

def topwear(request,data=None):
    if data == None:
        topwears=Product.objects.filter(category='TW')
    elif data=='G-collection' or data =='BlueMoon':
        topwears=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
    elif data=='above':
        topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
    return render(request, 'app/topwear.html',{'topwears':topwears})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'app/customerregistration.html',{'form':form})
def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr= request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobilenumber']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, mobilenumber=mobile,country=country,city=city,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

def search(request):
    nm=request.GET['nm']
    nm=nm.title()
    data=Product.objects.filter(title=nm).order_by('-id')
    return render(request,'app/search.html',{'data':data})

def plus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount= 90.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
         }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount= 90.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
         }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        c.delete()
        amount = 0.0
        shipping_amount= 90.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'amount':amount,
            'totalamount':amount + shipping_amount
         }
        return JsonResponse(data)
    
def add_comment(request, pk):
    product = Product.objects.get(id=pk)

    form = CommentForm(instance=product)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=product)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            c = Comment(product=product, user_name=name, comment_body=body, date_added=datetime.now())
            c.save()
            return redirect('product-detail',pk)
        else:
            print('form is invalid')    
    else:
        form = CommentForm()    


    context = {
        'form': form
    }

    return render(request, 'app/add_comment.html', context)
    