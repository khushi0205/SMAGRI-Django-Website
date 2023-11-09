import os


path = os.path.join(os.path.dirname(__file__), 'ds1.csv')

import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv(path)
fert = list(dataset.Fertilizer)
dist_n = list(dataset.District_Name)
soil_c = list(dataset.Soil_color)
crop = list(dataset.Crop)
N = list(dataset.Nitrogen)
P = list(dataset.Phosphorus)
K = list(dataset.Potassium)
pH = list(dataset.pH)
rain = list(dataset.Rainfall)

dn = list(dataset.District_Name.unique())
DN = {k: v for v, k in enumerate(dn)}
sc = list(dataset.Soil_color.unique())
SC = {k: v for v, k in enumerate(sc)}
c = list(dataset.Crop.unique())
C = {k: v for v, k in enumerate(c)}
f = list(dataset.Fertilizer.unique())
F = {k: v for v, k in enumerate(f)}

Dist = {'Kolhapur':0,'Solapur':1,'Satara':2,'Sangli':3,'Pune':4}
Soil = {'Black':0,'Red':1, 'MediumBrown': 2, 'DarkBrown': 3, 'LightBrown':4,'ReddishBrown':5}

F = list(dataset.Crop.unique())
F = {k: v for v, k in enumerate(F)}    
ferti = list(dataset.Fertilizer.unique())
Fert = {k: v for v, k in enumerate(ferti)}
