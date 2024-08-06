from django.urls import path 
from . import views

urlpatterns = [ 
    path('', views.broadcast_sms, name="default"),
]