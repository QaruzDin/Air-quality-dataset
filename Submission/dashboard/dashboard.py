import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import time

# Olah Data Cuaca Bulanan
def make_monthly_climateBeijing(df):
    monthly_climateBeijing = df.groupby(by=[df['DateTime'].dt.year.rename('Tahun'), 
                                            df['DateTime'].dt.month.rename('Bulan')]).agg({
                                            'RAIN': 'sum',
                                            'TEMP': ['min', 'mean', 'max'],
                                            'Rh' : 'mean'
                                        })
    monthly_climateBeijing.columns = ['Curah Hujan', 'Suhu Minimum', 'Suhu Rerata', 'Suhu Maksimum', 'Kelembapan']
    monthly_climateBeijing.reset_index(inplace=True)
    monthly_climateBeijing['Tanggal'] = pd.to_datetime(monthly_climateBeijing['Tahun'].astype(str) + '-' + \
                                                    monthly_climateBeijing['Bulan'].astype(str), format='%Y-%m')
    monthly_climateBeijing.drop(columns= ['Tahun', 'Bulan'], inplace=True)
    monthly_climateBeijing.insert(0, 'Tanggal', monthly_climateBeijing.pop('Tanggal'))
    return monthly_climateBeijing

# Olah Data Polutan
def make_pollutantSum_byYear(df):
    pollutantParam_Avg = ['PM2.5_24hr_avg','PM10_24hr_avg', 'SO2_24hr_avg', 'NO2_24hr_avg']
    pollutantParam_Max =['CO_8hr_max', 'O3_8hr_max']

    pollutantSum_byYear_df = df.groupby(by=['station', df['DateTime'].dt.year.rename('Tahun')]).agg({
        **{param: 'mean' for param in pollutantParam_Avg},
        **{param: 'max' for param in pollutantParam_Max}
    })
    pollutantSum_byYear_df.columns = ['PM2.5','PM10', 'SO2', 'NO2', 'CO', 'O3']
    pollutantSum_byYear_df.reset_index(inplace=True)
    return pollutantSum_byYear_df

# Olah Data AQI
def make_Beijing_in_AQICategorySum(df):
    Beijing_in_AQICategorySum = df.groupby(by=['station']).agg({
    'AQI_category': lambda x: x.unique().tolist(),
    'AQI_calculated' : 'mean'
    })
    Beijing_in_AQICategorySum.columns = ['Kategori AQI', 'Nilai AQI']
    Beijing_in_AQICategorySum.sort_values(by='Nilai AQI', inplace=True)
    Beijing_in_AQICategorySum.reset_index(inplace=True)
    Beijing_in_AQICategorySum['Kategori AQI'] = Beijing_in_AQICategorySum['Kategori AQI'].apply(lambda x: x[0])
    return Beijing_in_AQICategorySum

all_df = pd.read_csv('beijing_climateData.csv')
all_df.sort_values(by='DateTime', inplace=True)
all_df.reset_index(inplace=True)
all_df['DateTime'] = pd.to_datetime(all_df['DateTime'])

min_date = all_df['DateTime'].min()
max_date = all_df['DateTime'].max()

st.title('Weather Chart')
st.subheader('in the Beijing Area')

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/128/648/648198.png")
    st.header('Welcome to Weather Dashboard')
    
    
        
    #Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Please choose the date',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    main_df = all_df[(all_df['DateTime'] >= str(start_date)) & 
                (all_df['DateTime'] <= str(end_date))]

    monthly_climateBeijing = make_monthly_climateBeijing(main_df)
    pollutantSum_byYear = make_pollutantSum_byYear(all_df)
    Beijing_in_AQICategorySum = make_Beijing_in_AQICategorySum(all_df)


    st.caption('by :blue[Andi Artsam] | Dicoding Course')

x = monthly_climateBeijing['Tanggal']
y1 = monthly_climateBeijing['Curah Hujan']
y2 = monthly_climateBeijing['Suhu Minimum']
y3 = monthly_climateBeijing['Suhu Rerata']
y4 = monthly_climateBeijing['Suhu Maksimum']
y5 = monthly_climateBeijing['Kelembapan']
bt1, bt2, bt3 = 100, 300, 500

stationList = pollutantSum_byYear['station'].drop_duplicates().to_list()
labels = pollutantSum_byYear.columns[2:8].to_list()
barWidth = 0.15
xPos= np.arange(len(stationList))

station = Beijing_in_AQICategorySum['station']
nilaiAQI = Beijing_in_AQICategorySum['Nilai AQI']


tab1, tab2= st.tabs(['⛅Climate Change', '⚡Pollutant Emission'])

with tab1:
    st.header('Monthly Rainfall', divider = True)
    st.subheader(f'from {start_date} to {end_date}')

    with st.spinner('Wait for it...'):
        fig = plt.figure(figsize=(10, 6))
        plt.plot(x, y1, marker='o', linewidth=2, label='Rainfall', color='blue')

        plt.axhline(y=bt1, color='green', linestyle='--', label='Low Upper Limit')
        plt.axhline(y=bt2, color='orange', linestyle='--', label='Medium Upper Limit')
        plt.axhline(y=bt3, color='red', linestyle='--', label='High Upper Limit')

        plt.title("Monthly Rainfall in the Beijing Area for 5 years", fontsize=20)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Rainfall (mm/month)", fontsize=12)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    st.pyplot(fig)

    st.header('Temperature', divider = True)
    st.subheader(f'from {start_date} to {end_date}')
    
    with st.spinner('Wait for it...'):
        fig = plt.figure(figsize=(10, 6))
        plt.plot(x, y2, marker='o', linewidth=2, label='Min Temperature', color='yellow')
        plt.plot(x, y3, marker='o', linewidth=2, label='Mean Temperature', color='green')
        plt.plot(x, y4, marker='o', linewidth=2, label='Max Temperature', color='red')

        
        x_numeric = mdates.date2num(x) 
        coefficients = np.polyfit(x_numeric, y3, 1)
        trend = np.polyval(coefficients, x_numeric)
        plt.plot(x, trend, linestyle='--', color='black', label='Garis Tren')

        plt.title("Average Monthly Temperature in the Beijing Area for 5 Years", fontsize=20)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Temperature (°C)", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    st.pyplot(fig)

    st.header('Humidity', divider = True)
    st.subheader(f'from {start_date} to {end_date}')

    with st.spinner('Wait for it...'):
        ideal1, ideal2 = 45, 65

        fig = plt.figure(figsize=(10, 6))
        plt.plot(x, y5, marker='o', linewidth=2, label='Kelembapan', color='gray')

        plt.axhline(y=ideal1, color='green', linestyle='--', label='Ideal Upper Limit')
        plt.axhline(y=ideal2, color='green', linestyle='--', label='Ideal Lower Limit')

        plt.title("Average Humidity in the Beijing Area for 5 Years", fontsize=20)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Humidity (%)", fontsize=12)
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    st.pyplot(fig)

with tab2:
    st.header('Yearly Air Polution Level Based on Stations', divider = True)
    option = st.selectbox(
    'Select the polutant:',
    ('All', 'PM2.5','PM10', 'SO2', 'NO2', 'CO', 'O3')
    )
    
    with st.spinner('Wait for it...'):
        if option == 'All':
            
            fig, ax = plt.subplots(nrows=6, ncols=1, figsize=(15, 12))

            for i, label in enumerate(labels):
                for year in range(2013, 2018):
                    ax[i].bar(xPos + (barWidth * (year - 2013)), 
                            pollutantSum_byYear.loc[pollutantSum_byYear['Tahun'] == year, label].tolist(), 
                            width=barWidth,
                            label=f'{year}')
                ax[i].set_xticks(xPos + (barWidth * 2))
                ax[i].set_xticklabels(stationList)
                ax[i].set_xlabel('Station')
                if label == 'CO':
                    ax[i].set_ylabel('mg/m³')
                else:
                    ax[i].set_ylabel('µg/m³')
                ax[i].set_title(label, pad=10)
                ax[i].grid(visible=True, axis= 'y')

            plt.tight_layout()
            plt.legend(title='Year', loc='right', bbox_to_anchor=(1.1, 6))
            plt.suptitle("Air Pollution Levels in the Beijing Area for 5 Years", fontsize=20)
            plt.subplots_adjust(top=0.9)
            plt.show()
        else:
            fig = plt.figure(figsize=(15,2))
            pol = option
            for i, year in enumerate([2013, 2014, 2015, 2016, 2017]):
                plt.bar(xPos + (barWidth * i), pollutantSum_byYear.loc[pollutantSum_byYear['Tahun'] == year, pol].tolist(), width=barWidth, label=f'{year}')

            plt.xticks(xPos + (barWidth * 2), stationList)
            plt.xlabel('Station')
            if pol == 'CO':
                plt.ylabel('mg/m³')
            else:
                plt.ylabel('µg/m³')
            plt.title(pol)
            plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(visible=True, axis= 'y')

            plt.show()
        
    st.pyplot(fig)

    st.header('Air Quality Index', divider = True)

    with st.spinner('Wait for it...'):
        fig = plt.figure(figsize=(10,5))
        plt.barh(station, nilaiAQI, color= 'r')
        plt.ylabel('Station')
        plt.xlabel('Air Quality Index (AQI) Value')
        plt.title('Air Quality Index Based on Stations in the Beijing Area for 5 Years')
        plt.show()
    st.pyplot(fig)