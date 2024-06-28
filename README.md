
# Visualisation of Cryptocurrency Data with a Dynamic Database

This project focuses on fetching cryptocurrency data from an API, storing it in a database, and visualizing it using various tools. The project uses the TwelveData API to obtain cryptocurrency data, saves it in an SQLite database, calculates the Relative Strength Index (RSI) for each cryptocurrency, and visualizes the data using Matplotlib and PowerBI.

## Table of Contents
1. [Project Description](#project-description)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Scheduling Data Fetching](#scheduling-data-fetching)
6. [Historical Data Fetching](#historical-data-fetching)
7. [RSI Calculation](#rsi-calculation)
8. [Data Visualization](#data-visualization)
9. [PowerBI Integration](#powerbi-integration)
10. [Screenshots](#screenshots)

## Project Description

This project automates the process of fetching cryptocurrency data at regular intervals and saves it to an SQLite database. The data includes open, high, low, and close prices for each cryptocurrency. The project also calculates the RSI for each cryptocurrency and visualizes the data using Matplotlib. Additionally, the data is integrated with PowerBI for advanced visualization.

## Technologies Used

- Python
- SQLAlchemy
- Pandas
- Matplotlib
- PowerBI
- TwelveData API

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/SzczypekJ/Visualisation-of-cryptocurrency-data-with-a-dynamic-database.git
   cd Visualisation-of-cryptocurrency-data-with-a-dynamic-database
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask application**:
   ```sh
   python app.py
   ```

2. **Fetch and store cryptocurrency data**:
   - The script `fetch_data.py` fetches and stores data at regular intervals.
   - The script `historical_data.py` fetches historical data.

## Scheduling Data Fetching

The script `fetch_data.py` fetches data every hour and stores it in the database. It uses the TwelveData API to retrieve the data and SQLAlchemy to store it in an SQLite database. Additionally, it calculates the RSI for each cryptocurrency and updates the database with these values.

## Historical Data Fetching

The script `historical_data.py` fetches historical cryptocurrency data and saves it to the database. This allows for the analysis of past data and trends.

## RSI Calculation

The script `RSI.py` calculates the RSI for each cryptocurrency based on the data stored in the database. It uses Pandas to process the data and SQLAlchemy to update the database with the calculated RSI values.

## Data Visualization

The script `show_data.py` visualizes the cryptocurrency data and RSI values using Matplotlib. It generates candlestick charts and RSI graphs to provide a clear visual representation of the data.

## PowerBI Integration

The SQLite database containing the cryptocurrency data and calculated RSI values can be connected to PowerBI for advanced visualization. This allows for the creation of interactive dashboards and detailed analysis.

## Screenshots

![Visualization](path/to/your/image.png)

This image shows the final visualizations created using PowerBI, including candlestick charts and RSI indicators for different cryptocurrencies.

---

This `README.md` provides a comprehensive overview of the project, including instructions on how to set it up, fetch data, calculate RSI, and visualize the results.
