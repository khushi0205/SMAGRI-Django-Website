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

def closest_value(data, C):
    df = pd.DataFrame(data)

    # Convert columns to numeric (if not already)
    df = df.apply(pd.to_numeric, errors='coerce')

    # Calculate absolute differences between 'Your Crop' column and other numeric columns
    differences = df.drop(columns='Your Crop').apply(lambda col: abs(col - df['Your Crop'])).sum(axis=0)

    # Get the column with the smallest total absolute difference
    closest_column_name = differences.idxmin()

    # Get the entire column if it's the closest one
    closest_column_values = df[closest_column_name]

    # Create a new dataframe with 'Your Crop' and the closest column values
    new_df = pd.DataFrame({'Your Crop': df['Your Crop'], f'Standard Values for {C}': closest_column_values})

    print(new_df)
    return new_df