from django.urls import path,include,re_path
from . import views
app_name ='fashionStore'
urlpatterns = [
    path("",views.index,name='index')
    
]
