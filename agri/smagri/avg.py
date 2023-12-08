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
    differences = df.drop(columns='Your Crop').apply(lambda col: abs(col - df['Your Crop']))

    # Find the column index with the smallest absolute difference for each row
    closest_column_index = differences.values.argmin(axis=1)

    # Get the closest column names
    closest_column_name = df.drop(columns='Your Crop').columns[closest_column_index]

    # Extract values from the closest columns
    closest_values = [df[closest_column_name[i]][i] for i in range(len(closest_column_name))]

    # Create a new dataframe with 'Your Crop' and the closest column values
    new_df = pd.DataFrame({'Your Crop': df['Your Crop'], f'Standard Values for {C}': closest_values})

    print(new_df)
    return new_df