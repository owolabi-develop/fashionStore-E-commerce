from django.urls import path,include,re_path
from . import views
app_name ='fashionStore'

urlpatterns = [
    path("",views.index,name='index'),
    path("Userlogin/",views.UserLogin,name='Login'),
    path("Details/<int:product_id>/",views.details,name='details'),
    path("Category/<category_name>/",views.Category,name='Category'),
    path("Search/",views.searchPage,name="search-page"),
    path('SignUp/',views.Signup,name='signup'),
    re_path('^Email-Activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$',
        views.email_confirm, name='Email-activate'),
    path("forgotpassword/",views.forgotPassword,name='forgotpassword'),
    re_path('^Password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)$',
        views.password_reset.as_view(), name='password-reset'),
    path("Signup_success/",views.Signup_success,name='Signup_success'),
    path("Customer/Account/",views.UserProfile,name="Profile"),
    path("Customer/Wishlist/",views.Wishlist,name='Wishlist'),
    path("ProductBrand/<brand_brand>/",views.productbrands,name='product-brands'),
    path("ProductSizes/<size_size>/",views.productSize,name='product-size'),
    path("ProductPrice/",views.productprice,name='product-price'),
    path("Customer/add-to-Wishlist/<int:product_id>",views.add_Wishlist,name='add-Wishlist'),
     path("Customer/Remove-from-Wishlist/<int:product_id>",views.remove_Wishlist,name='remove-Wishlist'),
    path("Customer/Order/",views.UserOrder,name='order'),
    path("Customer/RecentlyViewed/",views.RecentlyView,name='RecentlyView'),
    path("Customer/addtocart/<int:product_id>/",views.addtocart,name='add-to-cart'),
    path("Customer/account/edit",views.userDetails,name='customer-details'),
    path("Customer/Change-Password/",views.changePassword,name='changePassword'),
    path("Customer/Address-Book/",views.AddressBook,name='Address-book'),
    path("Customer/Create-Address-Book/",views.AddressBook_create,name='Create-Address-book'),
    path("Customer/Close-Account/",views.CloseAccount,name='close-account'),
    path("Customer/NewSeltter/",views.AddressBook,name='new-seletter'),
    path("Customer/Cart/",views.ShopingCart,name='Shoping-cart'),
    path("Customer/EmptyCart/",views.EmptyCart,name='empty-cart'),
    path("Customer/Delete/Product/<int:product_id>/",views.delete_cart_pro,name='delete-product'),
    path("Customer/Checkout/",views.Checkoutpage,name=' Checkout-page'),
    path("Customer/PluQ/<int:product_id>/",views.plusQuantity,name='plusQuantity'),
    path("Customer/minusQ/<int:product_id>/",views.minusQuantity,name='minus-Quantity'),

    path("Customer/orders/details",views.order_details,name='order_details'),
    path("Logout/",views.User_logOut,name='logout'),
    path("PasswordRestDown/",views.password_down,name='password-down'),
    path('passwordchangcomplete/',views.password_reset_complete,name='password_reset_complete'),    
]
