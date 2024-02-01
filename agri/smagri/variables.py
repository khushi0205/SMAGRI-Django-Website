import os
path = os.path.join(os.path.dirname(__file__), 'ds1.csv')
import pandas as pd

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

Dist = {'Kolhapur':0,'Solapur':1,'Satara':2,'Sangli':3,'Pune':4}
Soil = {'Black':0,'Red':1, 'MediumBrown': 2, 'DarkBrown': 3, 'LightBrown':4,'ReddishBrown':5}

F = list(dataset.Crop.unique())
F = {k: v for v, k in enumerate(F)}    
ferti = list(dataset.Fertilizer.unique())
Fert = {k: v for v, k in enumerate(ferti)}

p1 = os.path.join(os.path.dirname(__file__), 'Ginger.csv')
ging = pd.read_csv(p1)
mn_ging = list(ging.Market_Name.unique())
MN_ging = {k: v for v, k in enumerate(mn_ging)}
ging['Price Date'] = pd.to_datetime(ging['Price Date'])
ging = ging.sort_values(by='Price Date')
ging_recent = ging.iloc[:-1]

p2 = os.path.join(os.path.dirname(__file__), 'Gram.csv')
gram = pd.read_csv(p2)
mn_gram = list(gram.Market_Name.unique())
MN_gram = {k: v for v, k in enumerate(mn_gram)}
gram['Price Date'] = pd.to_datetime(gram['Price Date'])
gram = gram.sort_values(by='Price Date')
gram_recent = gram.iloc[:-1]

p3 = os.path.join(os.path.dirname(__file__), 'Grapes.csv')
grapes= pd.read_csv(p3)
mn_grapes = list(grapes.Market_Name.unique())
MN_grapes = {k: v for v, k in enumerate(mn_grapes)}
grapes['Price Date'] = pd.to_datetime(grapes['Price Date'])
grapes = grapes.sort_values(by='Price Date')
grapes_recent = grapes.iloc[:-1]

p4 = os.path.join(os.path.dirname(__file__), 'Jowar.csv')
jowar = pd.read_csv(p4)
mn_jowar = list(jowar.Market_Name.unique())
MN_jowar = {k: v for v, k in enumerate(mn_jowar)}
jowar['Price Date'] = pd.to_datetime(jowar['Price Date'])
jowar = jowar.sort_values(by='Price Date')
jowar_recent = jowar.iloc[:-1]

p5 = os.path.join(os.path.dirname(__file__), 'Maize.csv')
maize = pd.read_csv(p5)
mn_maize = list(maize.Market_Name.unique())
MN_maize = {k: v for v, k in enumerate(mn_maize)}
maize['Price Date'] = pd.to_datetime(maize['Price Date'])
maize = maize.sort_values(by='Price Date')
maize_recent = maize.iloc[:-1]

p6 = os.path.join(os.path.dirname(__file__), 'Wheat.csv')
wheat = pd.read_csv(p6)
mn_wheat = list(wheat.Market_Name.unique())
MN_wheat = {k: v for v, k in enumerate(mn_wheat)}
wheat['Price Date'] = pd.to_datetime(wheat['Price Date'])
wheat = wheat.sort_values(by='Price Date')
wheat_recent = wheat.iloc[:-1]