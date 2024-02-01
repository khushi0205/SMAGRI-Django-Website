from django.urls import path
from . import views
#from .views import DownloadPDF
urlpatterns = [
    path('', views.Wel, name='Wel'),
    path('welcome/', views.Welcome, name='Welcome'),
    path('user/', views.User1, name='User1'),
    path('Res/', views.Res, name='Res'),
    path('MarketPrice/', views.MarkP, name='MP'),
    path('MarketPriceRes/', views.User2, name='MP_res'),
    path('MarketPriceResult/', views.User3, name='MP_result'),
    #path('Alternative_res/', views.Alt_Crop, name='AltCrop'),
    path('Alternative/', views.Alt_Res, name='AltC'),
    #path('download_pdf/', DownloadPDF.as_view(), name='download_pdf')


]