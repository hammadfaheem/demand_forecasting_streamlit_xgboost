# 🚴‍♂️ Demand Forecasting - Bike Rentals: The Streamlit App

This project is a **Streamlit web app** designed for visualizing and forecasting the **bike rental demand** in Washington, DC. The app provides an interactive interface for exploring bike rental data and weather trends and enables users to analyze and visualize bike-sharing trends.

## 🏠 Home Page
The home page provides an overview of the project, featuring an introduction to the app’s purpose and a fun **bike GIF**. The sidebar contains information about the app, allowing users to understand the project's context.

## 📊 Features

### 1. **Bike Rental Data**
   - **Time Span Selection**: Users can select a time frame (`daily`, `weekly`, `monthly`) to visualize average bike rentals by station.
   - **Interactive Map**: Using the **pydeck** library, the app displays an interactive map showing the average bike rentals per station. 
     - The map includes options for zooming and panning, with markers colored and elevated based on the number of bikes rented.
   - **Best/Worst Performing Stations**: Users can filter to see the best or worst-performing stations based on bike rental demand.
   - **Bar Charts**: Data is visualized using **Plotly** bar charts, allowing users to explore bike rental trends at different stations.
   - **Progressive Line Chart**: The app includes a dynamic line chart showing the total bike rentals over time, with real-time progress updates using a progress bar.

### 2. **Weather Data**
   - **Average Temperature By Month**: Visualizes the average observed temperature across different months using **Plotly** line charts.
   - **Average Rainfall By Month**: Similar to the temperature, this feature provides insights into monthly rainfall patterns, helping users understand how weather affects bike demand.

## 🔧 How It Works
1. **Data Input**: Users can select various options, such as the time frame or the number of stations to visualize.
2. **Dynamic Visualizations**: Depending on the user input, the app dynamically generates maps, bar charts, and line charts for an interactive data analysis experience.
3. **Pydeck & Plotly Integration**: The app leverages `pydeck` for rendering 3D maps and `Plotly` for creating aesthetically pleasing and interactive charts.

## 📂 Project Structure
```
demand_forecasting_streamlit_xgboost/
│
├── assets/                      # Contains images, GIFs, or other assets for the app
│   └── bike_2_giphy.gif          # Example GIF used in the app
│
├── data/                        # Data files used for visualizations and modeling
│   ├── combined_data.csv
│   ├── daily_avg_by_station.csv
│   ├── daily.csv
│   ├── monthly_avg_by_station.csv
│   ├── monthly.csv
│   ├── weekly_avg_by_station.csv
│   └── weekly.csv
│
├── models/                      # Directory for machine learning models
│   └── xgb_gs_best_estimator.pkl # Trained XGBoost model for forecasting
│
├── pages/                       # Streamlit page scripts for different parts of the app
│   ├── 2_📊_Visualizations.py    # Page for visualizing bike rental and weather data
│   └── 3_🚴_Forecast.py          # Page for visualizing forecasted bike demand using ML models
│
├── 1_🏠_Home.py                 # Home page of the Streamlit app
├── README.md                    # Documentation for the project
├── requirements.txt             # Dependencies for the project

```

## 📊 Libraries Used
- **Streamlit**: For creating the web app interface.
- **Pydeck**: For visualizing bike station data on interactive maps.
- **Plotly**: For creating bar and line charts.
- **Pandas**: For handling and analyzing data.
- **Base64**: For encoding media like GIFs.

## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run 1_🏠_Home.py
   ```

## 📈 Data Sources
The bike rental and weather data used in the app are stored in the `data/` folder and are dynamically loaded based on the user’s selection.

## 🌟 Future Enhancements
- **Predictive Models**: Incorporate machine learning models to forecast future bike rental demand based on historical data.
- **More Weather Factors**: Analyze the impact of other weather conditions such as wind speed or humidity on bike rental demand.

## 👨‍💻 Authors
- **Hammad Faheem** - Developer and Data Scientist

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you'd like any changes or additions!