from django.urls import path,include,re_path
from . import views
app_name ='fashionStore'

urlpatterns = [
    path("",views.index,name='index'),
    path("Userlogin/",views.UserLogin,name='Login'),
    path("Details/<int:product_id>/",views.details,name='details'),
    path("Category/<product_title>/",views.Category,name='Category'),
    path('SignUp/',views.Signup,name='signup'),
    re_path('^Email-Activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$',
        views.email_confirm, name='Email-activate'),
    path("forgotpassword/",views.forgotPassword,name='forgotpassword'),
    re_path('^Password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$',
        views.password_reset.as_view(), name='password-reset'),
    path("Signup_success/",views.Signup_success,name='Signup_success'),
    path("Customer/Account/",views.UserProfile,name="Profile"),
    path("Customer/Wishlist/",views.Wishlist,name='Wishlist'),
    path("Customer/Order/",views.UserOrder,name='order'),
    path("Customer/RecentlyViewed/",views.RecentlyView,name='RecentlyView'),
    path("Customer/Details/",views.userDetails,name='customer-details'),
    path("Customer/Change-Password/",views.changePassword,name='changePassword'),
    path("Customer/Address-Book/",views.AddressBook,name='Address-book'),
    path("Customer/Close-Account/",views.AddressBook,name='close-account'),
    path("Customer/NewSeltter/",views.AddressBook,name='new-seletter'),
     
    

    path("Logout/",views.User_logOut,name='logout'),
    path("PasswordRestDown/",views.password_down,name='password-down'),
    path('passwordchangcomplete/',views.password_reset_complete,name='password_reset_complete'),
    
]
