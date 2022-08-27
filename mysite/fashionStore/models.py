import secrets
import string
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
class FashionManager(BaseUserManager):
    def create_user(self, email,phoneNumber, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phoneNumber=phoneNumber,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  phoneNumber, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phoneNumber=phoneNumber,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    sex = (("Male","Male"),("Female","Female"))
    username = models.CharField(max_length=255,unique=True,blank=True,null=True)
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phoneNumberRegex = RegexValidator(regex = r"^\d{8,11}$")
    Gender = models.CharField(max_length=7,choices=sex,blank=True,null=True)
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True,blank=True,null=True)
    subscribe = models.BooleanField(verbose_name='i want to recieve fashionStore Newsletter',default=False,blank=True,null=True)
    objects = FashionManager()
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['phoneNumber']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Profile(models.Model):
    User = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Profile_pic = models.FileField("Profile Pic",upload_to='uploads/',default='uploads/default.png',validators=[FileExtensionValidator(allowed_extensions=['jpg','png'],message='Please Upload The Fellowing Image Format jpg ord png')])

    def __str__(self) -> str:
        return self.User.email

class Customer(models.Model):
   User = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

   def __str__(self) -> str:
        return self.User.first_name




class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.FileField(upload_to='product/')
    desc = models.TextField(max_length=255)
    category = models.ManyToManyField(Category)
   

    def __str__(self) -> str:
        return self.name
    
class WhishList(models.Model):
     product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
     customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True,blank=True)

class order(models.Model):
    del_method = (("standard door delivery","standard door delivery"),("Pickup Station","Pickup Station"))
    pay_method = (("Pay on delivery","on delivery"),("with Card","with Card"))
    tra_id =''.join(secrets.choice(string.digits) for i in range(10))
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order_date = models.DateField(auto_now_add=True)
    placed = models.BooleanField(default=False,null=True,blank=True)
    transction_id = models.CharField(max_length=20,unique=True,null=True,blank=True)
    delivery_method = models.BooleanField(max_length=255,choices=del_method,null=True,blank=True)
    payment_method = models.BooleanField(max_length=255,choices=pay_method,null=True,blank=True)
   
    @property
    def cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_price for item in orderitem])
        return total

    @property
    def cart_item(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    date_added =models.DateField(auto_now_add=True)
    @property
    def total_price(self):
        total = self.product.price * self.quantity
        return total


    

class State(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name

class city(models.Model):
    name = models.CharField(max_length=255)
    State = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) -> str:
        return self.name

class AddressBook(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(order,on_delete=models.SET_NULL,blank=True,null=True)
    State = models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    City= models.ForeignKey(city, on_delete=models.SET_NULL,blank=True,null=True)
    Street_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=17)
    default_address = models.BooleanField(default=True,null=True,blank=True)

    def __str__(self):
        return self.Street_address
    

