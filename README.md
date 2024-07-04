SOIL CLASSIFICATION AND CROP PREDICTION USING MACHINE
LEARNING WITH DJANGO<br><br>
Creating a website that allows Indian farmers to know their
soil better by letting them know the best suited crop and
fertilizer for their soil.<br>
- Developed a Django-based website for crop and fertilizer prediction and testing.
- Used LSTM for market price predictions on 100K+ data points spanning 10 years with 75 - 85% accuracy.
- Integrated IoT for real-time soil nutrient inputs, optimizing crop yield and predicting crop and fertilizer with 99% accuracy.
- Used Celery to manage loading time of LSTM models.
- Skills: Python, Deep Learning, LSTM, Time Series Forecasting, Data Analysis, Django, SQL, Machine Learning, Data Visualization, Celery

Files:
- /agri/smagri/views.py : contains all the views required for the ML and DL model to run
- /agri/smagri/variables.py : contains all the variables required by the views, mostly communicates data preprocessing values from pandas
- /agri/smagri/avg.py : contains all the major functions required by views.py for reusability of code, majorly includes: 1. Calculating Standard nutrient values for each crop and finding the crop which the user value is closest to. 2. Predict Quarterly Market prices for each crop for the next two years. 3. Predict quarterly market prices for each market present within the crop for the next two years. 4. Display an interactive graph that displays the averege % change in prices for each crop per quarter. 5. Integrate our NPK sensor with backend to extract NPK values in real time as inputs to our ML model.
- /agri/smagri/models.py : includes crop model to display all the crop data and info from the database.
- .h5 files: represent all the crop LSTM models
- .sav files: represent all the crop machine learning models
