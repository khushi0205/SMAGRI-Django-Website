#Dist = {'Kolhapur':0,'Solapur':1,'Satara':2,'Sangli':3,'Pune':4}
#DN = 'Kolhapur'
#print(Dist.get(DN))
import pandas as pd
from django.conf import settings
import os

path = os.path.join(os.path.dirname(__file__), 'ds1.csv')
dataset = pd.read_csv(path)
F = list(dataset.Fertilizer.unique())
F = {k: v for v, k in enumerate(F)}
print(F)
crop = 10
print(list(F.keys())[list(F.values()).index(crop)])