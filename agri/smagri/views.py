from django.shortcuts import render
import joblib
import pandas as pd
import os
from .variables import Dist, Soil, F, Fert, MN_ging, MN_gram, MN_grapes, MN_jowar, ging,jowar,gram,grapes,maize,wheat,MN_maize,MN_wheat
from .avg import umm, closest_value, predict, mn
from .models import Crop
from keras.models import load_model
from django.template.defaultfilters import safe
from django.core.cache import cache
from django.utils.safestring import mark_safe
import plotly.express as px

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
    # Create tab list using list comprehension
    tab = [request.session.get(key) for key in ['N', 'P', 'Po', 'pH', 'Rf', 'Temp']]

    # Create alt list using list comprehension
    alt = [Dist.get(D), Soil.get(S)] + tab


    if C == 'Selectanoption':
        crop = model_crop.predict([lis])
        res = list(F.keys())[list(F.values()).index(crop)]
        print(res)
        cotton_info = Crop.objects.get(name=res)
        print(cotton_info)
        lis.append(F.get(res))
        fert = model_fert.predict([lis])
        res_fert = list(Fert.keys())[list(Fert.values()).index(fert)]
        for key in umm.keys():
            if res in key:
                data[key] = umm[key]
        
        data['Your Crop'] = tab
        data_wocrop = closest_value(data, res)
        data_html = data_wocrop.to_html()
        message = None

        if request.method == 'POST' and 'clear_session' in request.POST:
            request.session.flush()  # Clear session data
            message = "Session data has been cleared."
        return render(request, 'user.html',{'res':res,'res_fert':res_fert, 'info':cotton_info, 'data': data_html, 'msg': message})
    
    else:
        #with crop
        lis.append(F.get(C))
        fert = model_fert.predict([lis])
        res = list(Fert.keys())[list(Fert.values()).index(fert)]
        crop_lis = Crop.objects.get(name=C)
        print(crop_lis)

        for key in umm.keys():
            if C in key:
                data[key] = umm[key]
        
        data['Your Crop'] = tab
        new_data = closest_value(data, C)
        data_html = new_data.to_html()

        #without crop
        crop = model_crop.predict([alt])
        result = list(F.keys())[list(F.values()).index(crop)]
        crop_res = Crop.objects.get(name=result)
        alt.append(F.get(result))
        fert = model_fert.predict([alt])
        res_fert = list(Fert.keys())[list(Fert.values()).index(fert)]

        for key in umm.keys():
            if result in key:
                data[key] = umm[key]
        
        data['Your Crop'] = tab
        alt_data = closest_value(data, result)
        data_alt_html = alt_data.to_html()
        message = None

        if request.method == 'POST' and 'clear_session' in request.POST:
            request.session.flush()  # Clear session data
            message = "Session data has been cleared."
        return render(request, 'res.html',{'res_crop':res,'res_fert':res_fert, 'info':crop_lis, 'info_alt':crop_res, 'data': data_html, 'data_alt': data_alt_html, 'msg': message})


def User2(request):
    C = request.GET['Crop']
    data_html = cache.get(f"data_html_{C}")
    plotly_html = cache.get(f"plotly_html_{C}")
    MN = cache.get(f"MN_{C}")

    if not data_html or not plotly_html or not MN:
        data = pd.DataFrame()
        if C == 'Jowar':
            model = load_model('Jowar_mn.h5')
            data = predict(jowar, model)
            MN = MN_jowar
        elif C == 'Gram':
            model = load_model('Gram_mn.h5')
            data = predict(gram, model)
            MN = MN_gram
        elif C == 'Grapes':
            model = load_model('Grapes_mn.h5')
            data = predict(grapes, model)
            MN = MN_grapes
        elif C == 'Ginger':
            model = load_model('Ginger_mn.h5')
            data = predict(ging, model)
            MN = MN_ging
        elif C == 'Wheat':
            model = load_model('Wheat_mn.h5')
            data = predict(wheat, model)
            MN = MN_wheat
        elif C == 'Maize':
            model = load_model('Maize_mn.h5')
            data = predict(maize, model)
            MN = MN_maize

        data_html = data.to_html(classes='table table-bordered hidden-row')
        data['Min Price Change'] = data['Predicted Min Price'].pct_change() * 100
        data['Max Price Change'] = data['Predicted Max Price'].pct_change() * 100
        data['Modal Price Change'] = data['Predicted Modal Price'].pct_change() * 100

        data['Quarter'] = data['Timestamp'].dt.to_period("Q").astype(str)
        grouped_df = data.groupby('Quarter').mean().reset_index()

        # Plotting with Plotly Express
        fig = px.line(grouped_df, x='Quarter', y=['Min Price Change', 'Max Price Change', 'Modal Price Change'],
                      labels={'value': 'Average Percentage Change'},
                      title='Average Predicted Price Changes Every Three Months',
                      markers=True, line_shape='linear')

        fig.update_layout(width=1000, height=600)
        # Convert the Plotly figure to HTML
        plotly_html = fig.to_html(full_html=False)

        # Cache the data
        cache.set(f"data_html_{C}", data_html, timeout=None)  # No timeout means cache indefinitely
        cache.set(f"plotly_html_{C}", plotly_html, timeout=None)
        cache.set(f"MN_{C}", MN, timeout=None)

    return render(request, 'market_prices_res.html', {'MN': MN, 'data': data_html, 'Crop': C, 'plotly_html': mark_safe(plotly_html)})

def User3(request):
    C = request.GET['Crop']
    MNe = request.GET['MName']
    data_html = cache.get(f"data_html_{C}_{MNe}")
    plotly_html = cache.get(f"plotly_html_{C}_{MNe}")
    MN = cache.get(f"MN_{C}")

    if not data_html or not plotly_html or not MN:
        data = pd.DataFrame()
        if C == 'Jowar':
            model = load_model('Jowar_mn.h5')
            data = mn(jowar, model, MNe)
            MN = MN_jowar
        elif C == 'Gram':
            model = load_model('Gram_mn.h5')
            data = mn(gram, model, MNe)
            MN = MN_gram
        elif C == 'Grapes':
            model = load_model('Grapes_mn.h5')
            data = mn(grapes, model, MNe)
            MN = MN_grapes
        elif C == 'Ginger':
            model = load_model('Ginger_mn.h5')
            data = mn(ging, model, MNe)
            MN = MN_ging
        elif C == 'Wheat':
            model = load_model('Wheat_mn.h5')
            data = mn(wheat, model, MNe)
            MN = MN_wheat
        elif C == 'Maize':
            model = load_model('Maize_mn.h5')
            data = mn(maize, model, MNe)
            MN = MN_maize

        data_html = data.to_html(classes='table table-bordered hidden-row')
        
        fig = px.line(data, x='Timestamp',
                      y=['Predicted Min Price', 'Predicted Max Price', 'Predicted Modal Price'],
                      labels={'value': 'Price (Rs./Quintal)'},
                      title=f'Predicted Prices for {MNe}',
                      markers=True, line_shape='linear')

        fig.update_layout(width=1000, height=600)

        # Convert the Plotly figure to HTML
        plotly_html = fig.to_html(full_html=False)

        # Cache the data
        cache.set(f"data_html_{C}_{MNe}", data_html, timeout=None)  # No timeout means cache indefinitely
        cache.set(f"plotly_html_{C}_{MNe}", plotly_html, timeout=None)
        cache.set(f"MN_{C}", MN, timeout=None)

    return render(request, 'market_prices_result.html', {'MN': MN, 'data': data_html, 'Crop': C, 'plotly_html': mark_safe(plotly_html)}) 
    
    
#class DownloadPDF(View):
#    def get(self, request, *args, **kwargs):
#        C = request.GET.get('Crop', '')
#        MNe = request.GET.get('MName', '')
#        data = pd.DataFrame()
#        MN = []
#        data_html = ''
#
#        if C == 'Jowar':
#            model = load_model('Jowar_mn.h5')
#            data, fps = predict(jowar, model)
#            MN = MN_jowar
#        if C == 'Gram':
#            model = load_model('Gram_mn.h5')
#            data, fps = predict(gram, model)
#            MN = MN_gram
#        if C == 'Grapes':
#            model = load_model('Grapes_mn.h5')
#            data, fps = predict(grapes, model)
#            MN = MN_grapes
#        if C == 'Ginger':
#            model = load_model('Ginger_mn.h5')
#            data, fps = predict(ging, model)
#            MN = MN_ging
#        # Similar code for other crops...
#
#        if MNe in data['Market_Name'].unique():
#            # Filter the DataFrame for the specific market
#            market_data = data[data['Market_Name'] == MNe]
#            data_html = market_data.to_html(classes='table table-bordered hidden-row')

        # Generate PDF directly from HTML content
#       pdf_data = f"""
#        <html>
#        <head>
#            <title>Predicted Prices for {MNe}</title>
#        </head>
#        <body>
#            {data_html}
#        </body>
#        </html>
#        """
#        response = HttpResponse(content_type='application/pdf')
#        response['Content-Disposition'] = f'attachment; filename="{C}_{MNe}_Predicted_Prices.pdf"'
#        pisa_status = pisa.CreatePDF(pdf_data, dest=response)
#        if not pisa_status.err:
#            return response

#        return HttpResponse('Error generating PDF', status=500)


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