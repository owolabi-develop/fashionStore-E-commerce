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


def index(request):
    return render(request,'FashionStore/index.html',{})

def details(request,product_id=1):
  return render(request,'FashionStore/details.html',{})



def Category(request,product_title='bag'):
  return render(request,'FashionStore/category.html',{})