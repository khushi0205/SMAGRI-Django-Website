#Dist = {'Kolhapur':0,'Solapur':1,'Satara':2,'Sangli':3,'Pune':4}
#DN = 'Kolhapur'
#print(Dist.get(DN))
import pandas as pd
from django.conf import settings
import os
from .avg import umm

path = os.path.join(os.path.dirname(__file__), 'ds1.csv')
C = 'Cotton'
data = pd.DataFrame()
    
for key in umm.keys():
    if C in key:
            data[key] = umm[key]    
print(data)
data_html = data.to_html()