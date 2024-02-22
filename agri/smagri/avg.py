import os
from .variables import ferti, F, MN_jowar, MN_grapes, MN_ging, MN_gram, jowar_recent,ging_recent,gram_recent,grapes_recent
path = os.path.join(os.path.dirname(__file__), 'ds1.csv')

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from sklearn.preprocessing import MinMaxScaler
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

def predict(crop_data, model):
    scaler = MinMaxScaler()
    most_recent_timestamp = pd.to_datetime(crop_data['Price Date'].max())
   
    # Number of quarters to predict into the future
    num_quarters = 8  # Adjust as needed

    # Function to generate future timestamps quarterly
    def generate_quarterly_timestamps(start_date, num_quarters):
        timestamps = [start_date + timedelta(days=(i * 90)) for i in range(1, num_quarters + 1)]
        return timestamps

    # Function to predict future prices based on historical data for a specific market
    def predict_future_prices_for_market(model, scaler, historical_data, market_name, timestamps):
        num_features = model.input_shape[2]
        sequence_length = model.input_shape[1]

        # Check the column names and adjust accordingly
        feature_columns = ['Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 'Modal Price (Rs./Quintal)']

        # Filter historical data for the specific market
        market_data = historical_data[historical_data['Market_Name'] == market_name]
        scaler.fit(market_data[feature_columns])
        # Scale the historical data
        scaled_data = scaler.transform(market_data[feature_columns])

        # Initialize an array to store predicted prices
        predicted_prices = np.zeros((len(timestamps), num_features))

        for i in range(len(timestamps)):
            # Use the last sequence_length data points for initialization
            sequence = scaled_data[-sequence_length:]

            # Ensure sequence length is consistent
            if len(sequence) < sequence_length:
                # Pad with zeros if sequence is shorter than expected
                sequence = np.pad(sequence, ((0, sequence_length - len(sequence)), (0, 0)))

            # Reshape for LSTM sequence
            reshaped_sequence = sequence.reshape((1, sequence_length, num_features))

            # Make prediction
            prediction = model.predict(reshaped_sequence)

            # Inverse transform prediction
            inverse_prediction = scaler.inverse_transform(prediction)

            # Store the predicted prices
            predicted_prices[i] = inverse_prediction.flatten()

            # Append the predicted prices to the scaled data for the next iteration
            scaled_data = np.vstack([scaled_data, inverse_prediction])

        return predicted_prices

    # Extract historical data (excluding the most recent data point)
    historical_data = crop_data.iloc[:-1]

    # Get unique market names
    market_names = historical_data['Market_Name'].unique()

    # Example usage for predicting future prices for each market
    all_predictions = []

    for market_name in market_names:
        # Generate quarterly timestamps for the market
        quarterly_timestamps = generate_quarterly_timestamps(most_recent_timestamp, num_quarters)
        
        # Predict future prices for the market
        future_prices = predict_future_prices_for_market(model, scaler, historical_data, market_name, quarterly_timestamps)

        # Create a dataframe to store the results
        columns = ['Predicted Min Price', 'Predicted Max Price', 'Predicted Modal Price']
        future_prices_df = pd.DataFrame(future_prices, columns=columns)
        future_prices_df['Timestamp'] = quarterly_timestamps
        future_prices_df['Market_Name'] = market_name
        future_prices_df = future_prices_df[['Timestamp', 'Market_Name'] + columns]

        # Append predictions for the current market to the overall list
        all_predictions.append(future_prices_df)

    # Concatenate all predictions into a single DataFrame
    all_predictions_df = pd.concat(all_predictions, ignore_index=True)
    return all_predictions_df

def mn(crop_data, model,MNe):
    scaler = MinMaxScaler()
    most_recent_timestamp = pd.to_datetime(crop_data['Price Date'].max())
   
    # Number of quarters to predict into the future
    num_quarters = 8  # Adjust as needed

    # Function to generate future timestamps quarterly
    def generate_quarterly_timestamps(start_date, num_quarters):
        timestamps = [start_date + timedelta(days=(i * 90)) for i in range(1, num_quarters + 1)]
        return timestamps

    # Function to predict future prices based on historical data for a specific market
    def predict_future_prices_for_market(model, scaler, historical_data, market_name, timestamps):
        num_features = model.input_shape[2]
        sequence_length = model.input_shape[1]

        # Check the column names and adjust accordingly
        feature_columns = ['Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 'Modal Price (Rs./Quintal)']

        # Filter historical data for the specific market
        market_data = historical_data[historical_data['Market_Name'] == market_name]
        scaler.fit(market_data[feature_columns])
        # Scale the historical data
        scaled_data = scaler.transform(market_data[feature_columns])

        # Initialize an array to store predicted prices
        predicted_prices = np.zeros((len(timestamps), num_features))

        for i in range(len(timestamps)):
            # Use the last sequence_length data points for initialization
            sequence = scaled_data[-sequence_length:]

            # Ensure sequence length is consistent
            if len(sequence) < sequence_length:
                # Pad with zeros if sequence is shorter than expected
                sequence = np.pad(sequence, ((0, sequence_length - len(sequence)), (0, 0)))

            # Reshape for LSTM sequence
            reshaped_sequence = sequence.reshape((1, sequence_length, num_features))

            # Make prediction
            prediction = model.predict(reshaped_sequence)

            # Inverse transform prediction
            inverse_prediction = scaler.inverse_transform(prediction)

            # Store the predicted prices
            predicted_prices[i] = inverse_prediction.flatten()

            # Append the predicted prices to the scaled data for the next iteration
            scaled_data = np.vstack([scaled_data, inverse_prediction])

        return predicted_prices

    # Extract historical data (excluding the most recent data point)
    historical_data = crop_data.iloc[:-1]

    # Get unique market names
    market_names = historical_data['Market_Name'].unique()

    # Example usage for predicting future prices for each market

    if MNe in market_names:
        # Generate quarterly timestamps for the market
        quarterly_timestamps = generate_quarterly_timestamps(most_recent_timestamp, num_quarters)
        
        # Predict future prices for the market
        future_prices = predict_future_prices_for_market(model, scaler, historical_data, MNe, quarterly_timestamps)

        # Create a dataframe to store the results
        columns = ['Predicted Min Price', 'Predicted Max Price', 'Predicted Modal Price']
        future_prices_df = pd.DataFrame(future_prices, columns=columns)
        future_prices_df['Timestamp'] = quarterly_timestamps
        future_prices_df['Market_Name'] = MNe
        future_prices_df = future_prices_df[['Timestamp', 'Market_Name'] + columns]

    return future_prices_df

def read_sensor_and_send_data():
    import serial
    import requests
    
    # Open serial connection
    ser = serial.Serial('COM3', 9600)  # Change 'COMX' to your serial port
    
    # Define Django endpoint
    url = 'https://mj6wmprx-8000.inc1.devtunnels.ms/Read_NPK/'
    
    # Read data from serial
    data = ser.readline().decode().strip()
    npk_values = data.split(',')
    
    # Extract NPK values
    nitrogen, phosphorus, potassium = map(int, npk_values)
    
    # Send data to Django
    payload = {'nitrogen': nitrogen, 'phosphorus': phosphorus, 'potassium': potassium}
    response = requests.post(url, data=payload)
    print(payload)
    return payload, nitrogen, phosphorus, potassium
