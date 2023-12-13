import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import streamlit as st

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
def make_Beijing_in_AQIValue(df):
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

st.title('Beijing Air Quality')

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    st.text('Pilih Rentang Waktu')
    #Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    main_df = all_df[(all_df['DateTime'] >= str(start_date)) & 
                (all_df['DateTime'] <= str(end_date))]

    monthly_climateBeijing = make_monthly_climateBeijing(main_df)
    pollutantSum_byYear = make_pollutantSum_byYear(main_df)
    Beijing_in_AQIValue = make_Beijing_in_AQIValue(main_df)


col1, col2, col3 = st.columns(3)