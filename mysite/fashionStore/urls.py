from django.urls import path,include,re_path
from . import views
app_name ='fashionStore'

urlpatterns = [
    path("",views.index,name='index'),
    path("Details/<int:product_id>/",views.details,name='details'),
    path("Category/<product_title>/",views.Category,name='Category')
    
]
