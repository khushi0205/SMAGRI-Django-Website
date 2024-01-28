from django.shortcuts import render
import joblib
import pandas as pd
# Create your views here.
from django.conf import settings
import os
from .variables import Dist, Soil, F, Fert, MN_ging, MN_gram, MN_grapes, MN_jowar, ging,jowar,gram,grapes
from .avg import umm, closest_value, predict
from .models import Crop
from keras.models import load_model
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.template.defaultfilters import safe

path = os.path.join(os.path.dirname(__file__), 'ds1.csv')

def Wel(request):
    return render(request, 'index2.html')
def Welcome(request):
    return render(request, 'index.html')
def Res(request):
    return render(request, 'user2.html')
def Alt_Res(request):
    return render(request, 'alter.html')
def MarkP(request):
    return render(request, 'market_prices.html')


def User1(request):
    model_crop = joblib.load('model.sav')
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


    request.session['N'] = request.GET['N']
    request.session['P'] = request.GET['P']
    request.session['Po'] = request.GET['Po']
    request.session['pH'] = request.GET['pH']
    request.session['Rf'] = request.GET['Rf']
    request.session['Temp'] = request.GET['Temp']
  
    data = pd.DataFrame()
    tab = []    

    tab.append(request.session.get('N'))
    tab.append(request.session.get('P'))
    tab.append(request.session.get('Po'))
    tab.append(request.session.get('pH'))
    tab.append(request.session.get('Rf'))
    tab.append(request.session.get('Temp'))


    if C == 'Selectanoption':
        crop = model_crop.predict([lis])
        res = list(F.keys())[list(F.values()).index(crop)]
        print(res)
        cotton_info = Crop.objects.get(name=res)
        print(cotton_info)
        for key in umm.keys():
            if res in key:
                data[key] = umm[key]
        
        data['Your Crop'] = tab
        new_data = closest_value(data, res)
        data_html = new_data.to_html()
        message = None

        if request.method == 'POST' and 'clear_session' in request.POST:
            request.session.flush()  # Clear session data
            message = "Session data has been cleared."
        return render(request, 'user.html',{'res':res, 'info':cotton_info, 'data': data_html, 'msg': message})
    
    else:
        lis.append(F.get(C))
        print(lis)
        fert = model_fert.predict([lis])
        res = list(Fert.keys())[list(Fert.values()).index(fert)]
        print(res)
        cotton_info = Crop.objects.get(name=C)
        print(cotton_info)
        for key in umm.keys():
            if C in key:
                data[key] = umm[key]
        
        data['Your Crop'] = tab
        new_data = closest_value(data, C)
        data_html = new_data.to_html()
        message = None

        if request.method == 'POST' and 'clear_session' in request.POST:
            request.session.flush()  # Clear session data
            message = "Session data has been cleared."
        return render(request, 'res.html',{'res':res, 'info':cotton_info,'data': data_html, 'msg': message})


def User2(request):
    C = request.GET['Crop']
    data = pd.DataFrame()
    if C == 'Jowar':
        model = load_model('Jowar_mn.h5')
        data, fps = predict(jowar, model)
        MN = MN_jowar
    if C == 'Gram':
        model = load_model('Gram_mn.h5')
        data, fps = predict(gram, model)
        MN = MN_gram
    if C == 'Grapes':
        model = load_model('Grapes_mn.h5')
        data, fps = predict(grapes, model)
        MN = MN_grapes
    if C == 'Ginger':
        model = load_model('Ginger_mn.h5')
        data, fps = predict(ging, model)
        MN = MN_ging
    data_html = data.to_html(classes='table table-bordered hidden-row')
    fps['Min Price Change'] = fps['Predicted Min Price'].pct_change() * 100
    fps['Max Price Change'] = fps['Predicted Max Price'].pct_change() * 100
    fps['Modal Price Change'] = fps['Predicted Modal Price'].pct_change() * 100

    # Group by three-month intervals
    fps['Quarter'] = fps['Timestamp'].dt.to_period("Q")
    grouped_df = fps.groupby('Quarter').mean()

    # Plotting
    plt.figure(figsize=(8, 6))

    plt.plot(grouped_df.index.astype(str), grouped_df['Min Price Change'], label='Min Price Change', marker='o')
    plt.plot(grouped_df.index.astype(str), grouped_df['Max Price Change'], label='Max Price Change', marker='o')
    plt.plot(grouped_df.index.astype(str), grouped_df['Modal Price Change'], label='Modal Price Change', marker='o')

    plt.title('Average Predicted Price Changes Every Three Months')
    plt.xlabel('Quarter')
    plt.ylabel('Average Percentage Change')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convert the BytesIO object to a base64-encoded string
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    
    return render(request, 'market_prices_res.html',{ 'MN': MN, 'data': safe(data_html), 'Crop': C , 'image_base64': image_base64}) 

def User3(request):
    C = request.GET['Crop']
    MNe = request.GET['MName']
    data = pd.DataFrame()
    if C == 'Jowar':
        model = load_model('Jowar_mn.h5')
        data, fps = predict(jowar, model)
        MN = MN_jowar
    if C == 'Gram':
        model = load_model('Gram_mn.h5')
        data, fps = predict(gram, model)
        MN = MN_gram
    if C == 'Grapes':
        model = load_model('Grapes_mn.h5')
        data, fps = predict(grapes, model)
        MN = MN_grapes
    if C == 'Ginger':
        model = load_model('Ginger_mn.h5')
        data, fps = predict(ging, model)
        MN = MN_ging
    
    if MNe in data['Market_Name'].unique():
    # Filter the DataFrame for the specific market
        market_data = data[data['Market_Name'] == MNe]
    data_html = market_data.to_html(classes='table table-bordered hidden-row')

    plt.figure(figsize=(12, 6))
    plt.plot(market_data['Timestamp'], market_data['Predicted Min Price'], label='Predicted Min Price')
    plt.plot(market_data['Timestamp'], market_data['Predicted Max Price'], label='Predicted Max Price')
    plt.plot(market_data['Timestamp'], market_data['Predicted Modal Price'], label='Predicted Modal Price')
    
    plt.title(f'Predicted Prices for {MNe}')
    plt.xlabel('Timestamp')
    plt.ylabel('Price (Rs./Quintal)')
    plt.legend()

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convert the BytesIO object to a base64-encoded string
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return render(request, 'market_prices_result.html',{ 'MN': MN, 'data': safe(data_html), 'Crop': C, 'image_base64': image_base64 }) 
    
    



"""
def Alt_Crop(request):
    C = request.GET['Crop']
    data = pd.DataFrame()
    tab = []
    for key in umm.keys():
        if C in key:
            data[key] = umm[key]    

    tab.append(request.session.get('N'))
    tab.append(request.session.get('P'))
    tab.append(request.session.get('Po'))
    tab.append(request.session.get('pH'))
    tab.append(request.session.get('Rf'))
    tab.append(request.session.get('Temp'))

    if 'N' in request.session:
        data['Your Crop'] = tab
        data_html = data.to_html()
        message = None

        if request.method == 'POST' and 'clear_session' in request.POST:
            request.session.flush()  # Clear session data
            message = "Session data has been cleared."

        return render(request, 'altres2.html', {'df_html': data_html,'message': message})
        
    else:
        data_html = data.to_html()
        return render(request, 'altres.html', {'df_html': data_html})"""