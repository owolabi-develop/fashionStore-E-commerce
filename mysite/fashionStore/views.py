from multiprocessing import reduction
from django.utils import timezone
from datetime import datetime
from django.core import serializers
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
from . models import Profile
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetCompleteView
from .forms import UserCreationForm,UserChangePassword,UserSetPassword,UserPasswordResetForm,User,UserEditForm,ProfileForm

def index(request):
    return render(request,'FashionStore/index.html',{})

def details(request,product_id=1):
  return render(request,'FashionStore/details.html',{})


def Category(request,product_title='bag'):
  return render(request,'FashionStore/category.html',{})

def post_save_Profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.get_or_create(User=instance)
post_save.connect(post_save_Profile, sender=settings.AUTH_USER_MODEL)

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

@login_required(login_url='/Userlogin/')
def UserProfile(request):
    if request.method =="POST":
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm()

    return render(request,"fashionStore/profile.html",{'form':form})

@login_required(login_url='/Userlogin/')
def Wishlist(request):
  return render(request,'fashionStore/whishlist.html')
@login_required(login_url='/Userlogin/')
def UserOrder(request):
  return render(request,'fashionStore/order.html')

def RecentlyView(request):
  return render(request,'fashionStore/RecentlyView.html')


@login_required(login_url='/Userlogin/')
def userDetails(request):
  if request.method == "POST":
    userEditform = UserEditForm(request.POST,instance=request.user)
    if userEditform.is_valid():
        userEditform.save()
        messages.success(request,'User info Update Successful')
  else:
      userEditform = UserEditForm(instance=request.user)
  return render(request,'fashionStore/customer-account-edit.html',{'userEditform':userEditform})

@login_required(login_url='/Userlogin/')
def changePassword(request):
  if request.method == "POST":
    PasswordChangeform = UserChangePassword(user=request.user, data=request.POST)
    if PasswordChangeform.is_valid():
        PasswordChangeform.save()
        update_session_auth_hash(request, PasswordChangeform.user)
        messages.success(request,'Password Update Successful')
  else:
      PasswordChangeform = UserChangePassword(user=request.user)
  return render(request,'fashionStore/changepass.html',{'PasswordChangeform':PasswordChangeform})

@login_required(login_url='/Userlogin/')
def CloseAccount(request):
  return render(request,'fashionStore/CloseAccount.html')

@login_required(login_url='/Userlogin/')
def AddressBook(request):
  return render(request,'fashionStore/AddressBook.html')

@login_required(login_url='/Userlogin/')
def NewsSeletter(request):
  return render(request,'fashionStore/NewsSeletter.html')