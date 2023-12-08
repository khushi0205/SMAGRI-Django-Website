from django.urls import path
from . import views

urlpatterns = [
    path('', views.Wel, name='Wel'),
    path('welcome/', views.Welcome, name='Welcome'),
    path('user/', views.User1, name='User1'),
    path('Res/', views.Res, name='Res'),
    
    #path('Change/', views.User2, name='Change'),
    path('Alternative_res/', views.Alt_Crop, name='AltCrop'),
    path('Alternative/', views.Alt_Res, name='AltC')


]