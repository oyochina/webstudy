from django.contrib import admin
from django.urls import path,re_path
from app02 import views



urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('index/',views.app01),
    #re_path('index/(?P<m>\d+)',views.index),
   re_path('index/',views.index),
    
]