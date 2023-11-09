import os
from .variables import ferti, F
path = os.path.join(os.path.dirname(__file__), 'ds1.csv')

import pandas as pd
import matplotlib.pyplot as plt



Dist = {'Kolhapur':0,'Solapur':1,'Satara':2,'Sangli':3,'Pune':4}
Soil = {'Black':0,'Red':1, 'MediumBrown': 2, 'DarkBrown': 3, 'LightBrown':4,'ReddishBrown':5}
dataset = pd.read_csv(path)
umm = {}
for j in ferti:
    df = pd.DataFrame(dataset.loc[dataset['Fertilizer'] == j])
    for i in F:
        DF = pd.DataFrame(df.loc[df['Crop']==i])
        if DF.empty == True:
            pass
        else:
            umm[i+' with '+j] = DF.mean()


