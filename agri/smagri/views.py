from django.shortcuts import render
import joblib
import pandas as pd
# Create your views here.
from django.conf import settings
import os
from .variables import Dist, Soil, F, Fert
from .avg import umm

path = os.path.join(os.path.dirname(__file__), 'ds1.csv')

def Wel(request):
    return render(request, 'index2.html')
def Welcome(request):
    return render(request, 'index.html')
def Res(request):
    return render(request, 'user2.html')
def Alt_Res(request):
    return render(request, 'alter.html')
def User1(request):
    model_crop = joblib.load('model.sav')
    lis = []
    D = request.GET['District_Name']
    S = request.GET['Soil_Color']
    lis.append(Dist.get(D))
    lis.append(Soil.get(S))
    lis.append(request.GET['N'])
    lis.append(request.GET['P'])
    lis.append(request.GET['Po'])
    lis.append(request.GET['pH'])
    lis.append(request.GET['Rf'])
    lis.append(request.GET['Temp'])
    crop = model_crop.predict([lis])
    res = list(F.keys())[list(F.values()).index(crop)]
    print(res)
    return render(request, 'user.html',{'res':res})

def User2(request):
    model_fert = joblib.load('model_fert.sav')
    lis = []
    D = request.GET['District_Name']
    S = request.GET['Soil_Color']
    lis.append(Dist.get(D))
    lis.append(Soil.get(S))
    lis.append(request.GET['N'])
    lis.append(request.GET['P'])
    lis.append(request.GET['Po'])
    lis.append(request.GET['pH'])
    lis.append(request.GET['Rf'])
    lis.append(request.GET['Temp'])
    C = request.GET['Crop']
    lis.append(F.get(C))
    print(lis)
    fert = model_fert.predict([lis])
    res = list(Fert.keys())[list(Fert.values()).index(fert)]
    print(res)
    return render(request, 'res.html',{'res':res})

def Alt_Crop(request):
    C = request.GET['Crop']
    data = pd.DataFrame()
    
    for key in umm.keys():
        if C in key:
            data[key] = umm[key]    
    
    data_html = data.to_html()
    return render(request, 'altres.html', {'df_html': data_html})