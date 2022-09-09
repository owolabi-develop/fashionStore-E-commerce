from ast import Return
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






class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
class ProductSize(models.Model):
    size = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.size

class ProductBrand(models.Model):
    brand = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.brand
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.FileField(upload_to='product/')
    desc = models.TextField(max_length=255)
    category = models.ManyToManyField(Category)
    sizes = models.ManyToManyField(ProductSize)
    brand = models.ManyToManyField(ProductBrand)
   

    def __str__(self) -> str:
        return self.name
    
class WhishList(models.Model):
     product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
     profile= models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True,blank=True)

     def __str__(self) -> str:
         return self.product.name


class order(models.Model):
    owner_user= models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True,blank=True)
    order_date = models.DateField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False,null=True,blank=True)
    order_id = models.CharField(max_length=20,unique=True,null=True,blank=True)
   
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

    def __str__(self) -> str:
        return "%s " % self.order_id

class UsersOrderItem(models.Model):
    user_orders = models.ForeignKey(order,on_delete=models.SET_NULL,blank=True,null=True)
    image = models.FileField(upload_to='UserOrder_product/')
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    desc = models.TextField(max_length=255)
    user = models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self) -> str:
        return self.name
 

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    date_added =models.DateField(auto_now_add=True)
    @property
    def total_price(self):
        total = self.product.price * self.quantity
        return total
    def __str__(self):
        return self.product.name
    

class AddressBook(models.Model):
    address_state = (
        (None,"Please Select State"),
        ("Delta","Delta"),
        ("Lagos","Lagos"),
        ("Abuja","Abuja"),
        ("Kano","Kano"),
        ("Rivers","Rivser"),
        ("Jos","Jos"),
        ("Sokoto","Sokoto"),
    )
    owner_user = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(order,on_delete=models.SET_NULL,blank=True,null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phoneNumberRegex = RegexValidator(regex = r"^\d{8,11}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length =11, unique=True,blank=True,null=True)
    Region = models.CharField(max_length=255,blank=True,null=True,choices=address_state)
    City= models.CharField(max_length=255)
    Delivery_address = models.CharField(max_length=255)
    Additional_information = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=17)
    default_address = models.BooleanField(default=True,null=True,blank=True)

    def __str__(self):
        return self.Delivery_address
    
    class Meta:
        ordering =['Delivery_address']
    

