from django.shortcuts import render
import joblib
import pandas as pd
# Create your views here.
from django.conf import settings
import os


path = os.path.join(os.path.dirname(__file__), 'ds1.csv')

def Welcome(request):
    return render(request, 'index.html')

def User(request):
    model_crop = joblib.load('model.sav')
    lis = []
    Dist = {'Kolhapur':0,'Solapur':1,'Satara':2,'Sangli':3,'Pune':4}
    Soil = {'Black':0,'Red':1, 'Medium Brown': 2, 'Dark Brown': 3, 'Light Brown':4,'Reddish Brown':5}
    dataset = pd.read_csv(path)
    F = list(dataset.Crop.unique())
    F = {k: v for v, k in enumerate(F)}
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