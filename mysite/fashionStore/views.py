import email
import requests
import json
from django.utils import timezone
from datetime import datetime
from django.core import serializers
from fashionStore.models import AddressBook
from django.db.models.query_utils import Q
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator as default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str,force_bytes
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from . tokens import account_activation_token
from django.urls import reverse, reverse_lazy
from . models import Profile,OrderItem,order,WhishList,Product
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetCompleteView
from .forms import AddressBookForm, UserCreationForm,UserChangePassword,UserSetPassword,UserPasswordResetForm,User,UserEditForm,ProfileForm
from . models import *
import string
from mysite.settings import MY_PAY_STACK_KEY_PUBLIC as publish_key
from mysite.settings import MY_PAY_STACK_KEY_SECRETE as publish_key2
import secrets
from paystackapi.paystack import Paystack
paystack = Paystack(secret_key=publish_key2)

cat1 = Category
cat = Category.objects.all()
cat2 = Category.objects.all()[:7]
customer_add = AddressBook

# generate transaction id =====================================
def generate_id(request):
  transaction_id = "".join(secrets.choice(string.digits) for i in range(11))
  return transaction_id   


  # index page to display all products=================


def post_save_Profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.get_or_create(User=instance)
post_save.connect(post_save_Profile, sender=settings.AUTH_USER_MODEL)

#Signup and email activation ====================
def Signup(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()
      current_site = get_current_site(request)
      subject_email = "Activate Your Email"
      message = render_to_string('fashionStore/email_template.html',{
          'user':user,
          'domain':current_site.domain,
          'uid':urlsafe_base64_encode(force_bytes(user.id)),
          'token':account_activation_token.make_token(user),
          'protocol':'http',
      })
      to_email = form.cleaned_data['email']
      from_email='owolabidevelop84@gmail.com'
      print(to_email)
      msg = EmailMultiAlternatives(subject_email,'Confirmation Form FashionStore',from_email,[to_email])
      msg.attach_alternative(message,'text/html')
      msg.send()
      return HttpResponseRedirect(reverse("fashionStore:Signup_success"))
  else:
    form = UserCreationForm()
  return render(request,'fashionStore/signup.html',{'form':form})

def Signup_success(request):
    return render(request,'fashionStore/Signup_success.html')


def UserLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("fashionStore:index"))
        else:
             messages.error(request,'Email or Password is incorrect try again')
    return render(request,'fashionStore/login.html')


def forgotPassword(request):
    if request.method =="POST":
        form = UserPasswordResetForm(data=request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['email']
            form.save(get_current_site(request),email_template_name='fashionStore/pwd_email_reset.html')
            return HttpResponseRedirect(reverse("fashionStore:password-down"))
    else:
        form = UserPasswordResetForm()
    return render(request,"fashionStore/forgotpassword.html",{"form":form})

def User_logOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("fashionStore:Login"))

def password_down(request):
    return render(request,'fashionStore/password-down.html')

class password_reset(PasswordResetConfirmView):
    template_name = "fashionStore/UserSetpassword.html"
    success_url = reverse_lazy("fashionStore:password_reset_complete")


def password_reset_complete(request):
    return render(request,'fashionStore/passwordchange.html')
     
        

def email_confirm(request,uidb64,token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(),pk=uid)
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return HttpResponseRedirect(reverse("fashionStore:Profile"))
    else:
        return HttpResponse("Activation link invalid")

def Signup_success(request):
    return render(request,'fashionStore/Signup_success.html')

def index(request):
  if request.user.is_authenticated:
     products = Product.objects.all()
     cats = cat
     paginator = Paginator(products,22)
     page_number = request.GET.get('page')
     allproducts = paginator.get_page(page_number)
     customer = request.user.profile
     orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
     user_order_item = orders.orderitem_set.all()
     current_order = [product.product for product in user_order_item]

  else:
    orders = {}
    products = Product.objects.all()
    cats = cat
    paginator = Paginator(products,22)
    page_number = request.GET.get('page')
    allproducts = paginator.get_page(page_number)
    current_order = None
  return render(request,'FashionStore/index.html',{'product':allproducts,'orders':orders,'cats':cats,'cat2':cat2,'current_order':current_order})

#product detials page=========================
def details(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  related_p = Product.objects.order_by('image').reverse()[:5]
  customer = request.user.profile
  orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  return render(request,'FashionStore/details.html',{'product':product,'related_p':related_p,'cat2':cat2,'orders':orders})

#product Category page ==============
def Category(request,category_name):
  if request.user.is_authenticated:
     profile = request.user.profile
     orders,create = order.objects.get_or_create(owner_user=profile,is_ordered=False)
  else:
    orders = {}
  category = get_object_or_404(cat1,name=category_name)
  cats = cat
  product_size = ProductSize.objects.all()
  brands = ProductBrand.objects.all()
  categorylistpagination = Product.objects.filter(category__name=category)
  paginator = Paginator(categorylistpagination,15)
  page_number = request.GET.get('page')
  categorylist = paginator.get_page(page_number)
  return render(request,'FashionStore/category.html',{'size':product_size,'brand':brands,'category':categorylist,'cats':cat,'orders':orders,'cat2':cat2,'category1':category})

@login_required(login_url='/Userlogin/')
def UserProfile(request):
    customer = get_object_or_404(User,id=request.user.id)
    orders,create = order.objects.get_or_create(owner_user=customer.profile,is_ordered=False)
    user_order_add = customer_add.objects.filter(owner_user=customer.profile)
    if request.method =="POST":
        form = ProfileForm(request.POST,request.FILES,instance=request.user.customer)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm()
    return render(request,"fashionStore/profile.html",{'form':form,"orders":orders,"user_order_add":user_order_add,'cat2':cat2})

@login_required(login_url='/Userlogin/')
def Wishlist(request):
  customer = request.user.profile
  saveItem = customer.whishlist_set.all()
  
  orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  user_order_item = orders.orderitem_set.all()
  current_order = [product.product for product in user_order_item]
  print(current_order)
  return render(request,'fashionStore/whishlist.html',{'saveItem':saveItem,"orders":orders,'cat2':cat2,'current_order':current_order})

@login_required(login_url='/Userlogin/')
def add_Wishlist(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  customer = request.user.profile
  item,created = WhishList.objects.get_or_create(product=product, profile=customer)
  if created:
    messages.success(request,"Product add to Wishlist")
  else:
     messages.success(request,"Product Already in Wishlist")

  return HttpResponseRedirect(reverse("fashionStore:index"))

@login_required(login_url='/Userlogin/')
def remove_Wishlist(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  customer = request.user.profile
  item= WhishList.objects.filter(product=product,profile=customer)
  deleteWishlist = item.delete()
  if deleteWishlist:
    messages.success(request,"Product remove from wishlist")
  return HttpResponseRedirect(reverse("fashionStore:Wishlist"))

@login_required(login_url='/Userlogin/')
def UserOrder(request):
  customer = request.user.profile
  orders1,created = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  
  orders = order.objects.filter(is_ordered=True)

  user_orders = UsersOrderItem.objects.filter(user=customer)
  return render(request,'fashionStore/order.html',{'orders':orders1,'cat2':cat2,"user_orders":user_orders,'ordersID':orders})

def RecentlyView(request):
  customer = request.user.profile
  orders,create = order.objects.get_or_create(owner_user=customer,is_odered=False)
  return render(request,'fashionStore/RecentlyView.html',{'orders':orders})


@login_required(login_url='/Userlogin/')
def userDetails(request):
  customer = request.user.profile
  orders= order.objects.get(owner_user=customer,is_ordered=False)
  if request.method == "POST":
    userEditform = UserEditForm(request.POST,instance=request.user)
    if userEditform.is_valid():
        userEditform.save()
        messages.success(request,'User info Update Successful')
  else:
      userEditform = UserEditForm(instance=request.user)
  return render(request,'fashionStore/customer-account-edit.html',{'userEditform':userEditform,"orders":orders,'cat2':cat2})

@login_required(login_url='/Userlogin/')
def changePassword(request):
  customer = request.user.profile
  orders= order.objects.get(owner_user=customer,is_ordered=False)
  if request.method == "POST":
    PasswordChangeform = UserChangePassword(user=request.user, data=request.POST)
    if PasswordChangeform.is_valid():
        PasswordChangeform.save()
        update_session_auth_hash(request, PasswordChangeform.user)
        messages.success(request,'Password Update Successful')
  else:
      PasswordChangeform = UserChangePassword(user=request.user)
  return render(request,'fashionStore/changepass.html',{'PasswordChangeform':PasswordChangeform,"orders":orders,'cat2':cat2})

@login_required(login_url='/Userlogin/')
def CloseAccount(request):
  return render(request,'fashionStore/CloseAccount.html')



@login_required(login_url='/Userlogin/')
def AddressBook_create(request):
  customer = request.user.profile
  orders= order.objects.get(owner_user=customer,is_ordered=False)
  if request.method =="POST":
    form = AddressBookForm(request.POST)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.owner_user = customer
      instance.order=orders
      instance.save()
      messages.success(request,'Address created')
    return HttpResponseRedirect(reverse("fashionStore:Create-Address-book"))
  else:
    form = AddressBookForm(initial={'first_name':customer.User.first_name,'last_name':customer.User.last_name,'phoneNumber':customer.User.phoneNumber})

  return render(request,'fashionStore/AddressBook_create.html',{'orders':orders,'form':form,'cat2':cat2})

@login_required(login_url='/Userlogin/')
def AddressBook_Edit(request,address_id):
  customer_address = get_object_or_404(customer_add,pk=address_id)
  customer = request.user.profile
  orders= order.objects.get(owner_user=customer,is_ordered=False)
  if request.method =="POST":
    form = AddressBookForm(request.POST,instance=customer_address)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.customer = customer
      instance.order=orders
      instance.save()
      messages.success(request,'Address Updated')
    return HttpResponseRedirect(reverse("fashionStore:Profile"))
  else:
    form = AddressBookForm(instance=customer_address)

  return render(request,'fashionStore/AddressBook_edit.html',{'orders':orders,'form':form,'customer_address':customer_address,'cat2':cat2})

# user address book
def userAddressBook(request):
  customer = request.user.profile
  address = customer.addressbook_set.all()
  user_address = [address for item in address]
  
  orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)



  return render(request,'fashionStore/userAddressbook.html',{'address':address,'cat2':cat2,'orders':orders}) 

@login_required(login_url='/Userlogin/')
def NewsSeletter(request):
  customer = request.user.profile
  orders=order.objects.get_or_create(owner_user=customer,is_ordered=False)
  return render(request,'fashionStore/NewsSeletter.html',{'orders':orders,'cat2':cat2})


def ShopingCart(request):
  if not request.user.is_authenticated:
    customer = None
    orders = None
    item = None
  else:
    customer = request.user.profile
    orders= order.objects.get(owner_user=customer,is_ordered=False)
    item = orders.orderitem_set.all()
  return render(request,'fashionStore/shopingCart.html',{'item':item,'orders':orders,'cat2':cat2})


@login_required(login_url='/Userlogin/')
def addtocart(request,product_id):
  product = Product.objects.get(id=product_id)
  customer = request.user.profile
  orders,created = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  item,create = OrderItem.objects.get_or_create(order=orders,product=product)
  print(product.id,product.name,product.image)
  orders.usersorderitem_set.create(image=product.image,name=product.name,price=product.price,desc=product.desc,user=customer)
  if create:
     messages.success(request,'product was add to card')
  return HttpResponseRedirect(reverse('fashionStore:index'))

def delete_cart_pro(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  customer = request.user.profile
  orders,created = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  item= OrderItem.objects.filter(product=product,order=orders)
  delete_product = item.delete()
  if delete_product:
    messages.success(request,'Product was remove cart')
  return HttpResponseRedirect(reverse("fashionStore:Shoping-cart"))

def plusQuantity(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  customer = request.user.profile
  orders,created = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  plusQ = orders.orderitem_set.get(product=product)
  plusQ.quantity +=1
  plusQ.save()
  if plusQ:
    messages.success(request,'Product added to cart')
  return HttpResponseRedirect(reverse("fashionStore:Shoping-cart"))

def minusQuantity(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  customer = request.user.profile
  orders,created = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  plusQ = orders.orderitem_set.get(product=product)
  plusQ.quantity-=1
  plusQ.save()
  if plusQ:
    messages.success(request,'Product remove from cart')
  return HttpResponseRedirect(reverse("fashionStore:Shoping-cart"))

def EmptyCart(request):
  customer = request.user.profile
  orders,created = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  item= OrderItem.objects.filter(order=orders)
  empty_cart = item.delete()
  if empty_cart:
    messages.success(request,'All item in cart has been remove cart empty...')
  return HttpResponseRedirect(reverse("fashionStore:Shoping-cart"))

@login_required(login_url='/Userlogin/')
def Checkoutpage(request):
  if not request.user.is_authenticated:
    customer = None
    orders = None
    item = None
  else:
    customer = get_object_or_404(User,email=request.user)
    orders,create = order.objects.get_or_create(owner_user=request.user.profile,is_ordered=False)
    item = orders.orderitem_set.all()
  customer = request.user.profile
  orders= order.objects.get(owner_user=customer,is_ordered=False)
  if request.method =="POST":
    form = AddressBookForm(request.POST)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.owner_user = customer
      instance.order=orders
      instance.save()
      messages.success(request,'Address created')
    return HttpResponseRedirect(reverse("fashionStore:payment-method"))
  else:
    form = AddressBookForm(initial={'first_name':customer.User.first_name,'last_name':customer.User.last_name,'phoneNumber':customer.User.phoneNumber})
  return render(request,'fashionStore/checkout.html',{'item':item,'orders':orders,"form":form})


@login_required(login_url='/Userlogin/')
def order_details(request):
  return render(request,'fashionStore/order-details.html')

def searchPage(request):
  query = request.GET.get('query')
  product_size = ProductSize.objects.all()
  product_brand = ProductBrand.objects.all()
  if query:
    
    result = Product.objects.filter(Q(name__icontains=query)|Q(category__name__icontains=query)|Q(brand__brand__icontains=query))
    total_product = result.count()
  else:
    result = "No products Found"
  cats = cat
  if not request.user.is_authenticated:
    customer = None
    orders = None
    item = None
  else:
    customer = request.user.profile
    orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  return render(request,'fashionStore/search_result.html',{"cats":cats,"cat2":cat2,'result':result,'size':product_size,'brand':product_brand,'orders':orders})


def productbrands(request,brand_brand):
  product_brand = get_object_or_404(ProductBrand,brand=brand_brand)
  product_size = ProductSize.objects.all()
  brands = ProductBrand.objects.all()
  cats = cat
  if not request.user.is_authenticated:
    customer = None
    orders = None
    item = None
  else:
    customer = request.user.profile
    orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  return render(request,"fashionStore/productbrands.html",{'brand':brands,"product_brand":product_brand,'size':product_size,'orders':orders,"cats":cats,"cat2":cat2,})

def productSize(request,size_size):
  product_size = get_object_or_404(ProductSize,size=size_size)
  Sizes = ProductSize.objects.all()
  brands = ProductBrand.objects.all()
  cats = cat
  if not request.user.is_authenticated:
    customer = None
    orders = None
    item = None
  else:
    customer = request.user.profile
    orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  return render(request,"fashionStore/productSizes.html",{'size':Sizes,'brand':brands,"product_size":product_size,'orders':orders,"cats":cats,"cat2":cat2})


# productprice ====
def productprice(request):
  hi = request.GET.get('hi')
  low = request.GET.get('low')
  if low and hi:
    price = Product.objects.filter(Q(price__range=(low,hi)))
    print(price)

  Sizes = ProductSize.objects.all()
  brands = ProductBrand.objects.all()
  cats = cat
  if not request.user.is_authenticated:
    customer = None
    orders = None
    item = None
  else:
    customer = request.user.profile
    orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  return render(request,"fashionStore/productprice.html",{'size':Sizes,'brand':brands,'orders':orders,"cats":cats,"cat2":cat2,'price':price})

#payment method=================
@login_required(login_url='/Userlogin/')
def Payment_method(request):
  customer = request.user.profile
  orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  item = orders.orderitem_set.all()
  if request.method == "POST":
    email = request.POST.get('email',None)
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {"Authorization": f"Bearer {publish_key2}",}
    payload = {
      "email":email,
      "amount":orders.cart_total*100,
      "reference":secrets.token_urlsafe(11),
      "callback_url":"http://localhost:1998/Payment-verify/"
     
      }
    response = requests.post(url=url,headers=headers,data=payload)
    r = json.loads(response.text)
    print(r)
    if response.status_code ==200:
      return HttpResponseRedirect(r['data']['authorization_url'])
  return render(request,'fashionStore/payment.html',{'item':item,'orders':orders})

  
  

@login_required(login_url='/Userlogin/')
def verify_transaction(request):
  customer = request.user.profile
  orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  orders.order_id = generate_id(request)
  orders.save()
  reference = request.GET.get('reference',None)
  response = paystack.transaction.verify(reference)
  if response['data']['status'] =="success":
    return HttpResponseRedirect(reverse("fashionStore:transaction_update",args=(orders.order_id,)))

 

#transaction uppdate
@login_required(login_url='/Userlogin/')
def transaction_update(request,order_id):
  customer = request.user.profile
  orders,create = order.objects.get_or_create(owner_user=customer,is_ordered=False)
  orders.is_ordered = True
  orders.order_date = timezone.now()
  orders.save()
  return HttpResponseRedirect(reverse("fashionStore:order"))

