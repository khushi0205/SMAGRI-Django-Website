def read_sensor_and_send_data():
    import serial
    import requests
    
    # Open serial connection
    ser = serial.Serial('COMX', 9600)  # Change 'COMX' to your serial port
    
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
    
    print("Data sent to Django:", payload)