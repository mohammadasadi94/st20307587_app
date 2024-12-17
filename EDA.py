import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def EDA_Part2(combined_dataFrame):

  columns=['PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','WSPM','wd','WSPM']
  for item in columns:
    combined_dataFrame[item] = combined_dataFrame[item].ffill()

  pollutants=['PM2.5','PM10','SO2','NO2','CO','O3']
  pollutants_mean_values=combined_dataFrame[pollutants].mean()
  option = st.radio("What type of analysis would you like to perform?",("Pollutant-Based Analysis", "Station-Based Analysis"))
  if option == "Station-Based Analysis":
    tab1, tab2, tab3,tab4,tab5  = st.tabs([" Year-wise Average Concentration of Pollutants","Overall Average Concentration of Pollutants", "Percentage Contribution of Each Pollutant", "Average Overall Pollution Levels","Pollutants AQI Comparison Across Stations "])
    with tab1:
      for item in pollutants:
        df = combined_dataFrame[[item, 'year', 'station']].groupby(["year", "station"]).mean().reset_index()
        plt.figure(figsize=(20, 5))
        sns.pointplot(x='year', y=item, hue='station', data=df, markers='o', linestyles='-', alpha=0.8)
        plt.xlabel('year')
        plt.ylabel(f'{item} (ug/m³)')
        plt.title(f'{item} Yearly Average Concentration by Station')
        plt.legend(title="Station", fontsize=8)
        plt.xticks(rotation=45)
        plt.show()
        st.pyplot(plt.gcf())
    with tab2:
      pollutant_means_station = combined_dataFrame.groupby('station')[pollutants].mean().sort_values(by=pollutants, ascending=False)
      for item in pollutants:
        plt.figure(figsize=(10, 6))
        pollutant_means_station[item].plot(kind='bar')
        plt.title(f'Average {item} Concentration by Station')
        plt.ylabel(f'{item} (µg/m³)')
        plt.xlabel('station')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt.gcf())

    with tab3:
      index=0
      pollutant_means_station = combined_dataFrame.groupby('station')[pollutants].mean().sort_values(by=pollutants, ascending=False)
      for item in pollutants:
        plt.figure(figsize=(8, 8))
        plt.pie(pollutant_means_station[item], labels=pollutants_mean_values.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title('Percentage Contribution of Each Pollutant in '+pollutant_means_station.index[index])
        plt.show()
        st.pyplot(plt.gcf())
        index=index+1

    with tab4:
      combined_dataFrame['overal pollution'] = combined_dataFrame[pollutants].sum(axis=1)
      overall_pollution_station=combined_dataFrame.groupby('station')['overal pollution'].mean().sort_values(ascending=True)
      plt.figure(figsize=(10, 6))
      overall_pollution_station.plot(kind='bar')
      plt.title('Average Overall Pollution Levels by Station')
      plt.xlabel('Station', fontsize=14)
      plt.ylabel('Total Pollution Level (µg/m³)')
      plt.xticks(rotation=45)
      plt.tight_layout()
      plt.show()
      st.pyplot(plt.gcf())
    with tab5:

      def aqi_pm25(pm25):
        if pm25 <= 12:
            return (pm25 / 12) * 50 
        elif pm25 <= 35.4:
            return 50 + ((pm25 - 12) / (35.4 - 12)) * 50 
        elif pm25 <= 150.4:
            return 150 + ((pm25 - 55.4) / (150.4 - 55.4)) * 50  
        elif pm25 <= 250.4:
            return 200 + ((pm25 - 150.4) / (250.4 - 150.4)) * 100
        else:
            return 300

      def aqi_pm10(pm10):
        if pm10 <= 54:
          return (pm10 / 54) * 50 
        elif pm10 <= 154:
          return 50 + ((pm10 - 54) / (154 - 54)) * 50  
        elif pm10 <= 354:
          return 150 + ((pm10 - 254) / (354 - 254)) * 50  
        elif pm10 <= 424:
          return 200 + ((pm10 - 354) / (424 - 354)) * 100  
        else:
          return 300  

      def aqi_co(co):
        if co <= 4.4:
          return (co / 4.4) * 50  
        elif co <= 9.4:
          return 50 + ((co - 4.4) / (9.4 - 4.4)) * 50 
        elif co <= 15.4:
          return 150 + ((co - 12.4) / (15.4 - 12.4)) * 50  
        elif co <= 30.4:
          return 200 + ((co - 15.4) / (30.4 - 15.4)) * 100
        else:
          return 300 

      def aqi_no2(no2):
        if no2 <= 53:
          return (no2 / 53) * 50  
        elif no2 <= 100:
          return 50 + ((no2 - 53) / (100 - 53)) * 50  
        elif no2 <= 649:
          return 150 + ((no2 - 360) / (649 - 360)) * 50 
        elif no2 <= 1249:
          return 200 + ((no2 - 649) / (1249 - 649)) * 100 
        else:
          return 300 

      def aqi_so2(so2):
        if so2 <= 35:
          return (so2 / 35) * 50  
        elif so2 <= 75:
          return 50 + ((so2 - 35) / (75 - 35)) * 50  
        elif so2 <= 304:
          return 150 + ((so2 - 185) / (304 - 185)) * 50  
        elif so2 <= 604:
          return 200 + ((so2 - 304) / (604 - 304)) * 100
        else:
          return 300 

      def aqi_o3(o3):
        if o3 <= 54:
          return (o3 / 54) * 50  
        elif o3 <= 70:
          return 50 + ((o3 - 54) / (70 - 54)) * 50  
        elif o3 <= 105:
          return 150 + ((o3 - 85) / (105 - 85)) * 50 
        elif o3 <= 200:
          return 200 + ((o3 - 105) / (200 - 105)) * 100
        else:
          return 300

      def aqi_status(aqi):
        if aqi <= 50:
          return 'Good'
        elif aqi <= 100:
          return 'Moderate'
        else:
          return 'Unhealthy'
    # Calculate AQI values and statuses
      combined_dataFrame['AQI_PM2.5'] = combined_dataFrame['PM2.5'].apply(aqi_pm25)
      combined_dataFrame['AQI_PM10'] = combined_dataFrame['PM10'].apply(aqi_pm10)
      combined_dataFrame['AQI_CO'] = combined_dataFrame['CO'].apply(aqi_co)
      combined_dataFrame['AQI_NO2'] = combined_dataFrame['NO2'].apply(aqi_no2)
      combined_dataFrame['AQI_SO2'] = combined_dataFrame['SO2'].apply(aqi_so2)
      combined_dataFrame['AQI_O3'] = combined_dataFrame['O3'].apply(aqi_o3)

      combined_dataFrame['AQI_OVERALL'] = combined_dataFrame[['AQI_PM2.5', 'AQI_PM10', 'AQI_CO', 'AQI_NO2', 'AQI_SO2', 'AQI_O3']].max(axis=1)

      combined_dataFrame['AQI_STATUS_PM2.5'] = combined_dataFrame['AQI_PM2.5'].apply(aqi_status)
      combined_dataFrame['AQI_STATUS_PM10'] = combined_dataFrame['AQI_PM10'].apply(aqi_status)
      combined_dataFrame['AQI_STATUS_CO'] = combined_dataFrame['AQI_CO'].apply(aqi_status)
      combined_dataFrame['AQI_STATUS_NO2'] = combined_dataFrame['AQI_NO2'].apply(aqi_status)
      combined_dataFrame['AQI_STATUS_SO2'] = combined_dataFrame['AQI_SO2'].apply(aqi_status)
      combined_dataFrame['AQI_STATUS_O3'] = combined_dataFrame['AQI_O3'].apply(aqi_status)
      combined_dataFrame['AQI_STATUS_OVERALL'] = combined_dataFrame['AQI_OVERALL'].apply(aqi_status)

      pollutants = ['PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3']
      aqi_status_columns = ['AQI_STATUS_PM2.5', 'AQI_STATUS_PM10', 'AQI_STATUS_CO', 'AQI_STATUS_NO2', 'AQI_STATUS_SO2', 'AQI_STATUS_O3']

      for i in range(len(pollutants)):
          pollutant = pollutants[i]
          aqi_column = aqi_status_columns[i]
          status_counts = combined_dataFrame.groupby('station')[aqi_column].value_counts().unstack().fillna(0)
          ax = status_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
          ax.set_title(f'{pollutant} AQI Status Comparison Across Stations')
          ax.set_xlabel('Station')
          ax.set_ylabel('Frequency')
          ax.legend(title=f'{pollutant} Status', bbox_to_anchor=(1.05, 1), loc='upper left')
          plt.tight_layout()
          plt.show()
          st.pyplot(plt.gcf())

      

  elif option == "Pollutant-Based Analysis":
    tab1, tab2,tab3  = st.tabs(["Pollutants Yearly Average Concentration","Overall Average Concentration of Pollutants", "overall hourly distribution of pollutant concentrations(Histogram)"])
    with tab1:
      for item in pollutants:
        df = combined_dataFrame[[item, 'year']].groupby(["year"]).mean().reset_index()
        plt.figure(figsize=(15, 5))
        sns.pointplot(x='year', y=item, data=df, markers='o',color='blue', linestyles='-', alpha=0.7)
        plt.xlabel('Year')
        plt.ylabel(f'{item} (ug/m³)')
        plt.title(f'{item} Yearly Average Concentration')
        plt.xticks(rotation=45)
        plt.show()
        st.pyplot(plt.gcf())

    with tab2:
      plt.figure(figsize=(6, 3))
      pollutants_mean_values.plot(kind='bar')
      plt.title('Average Concentration of Pollutants')
      plt.ylabel('Concentration')
      plt.show()
      st.pyplot(plt.gcf())

      plt.figure(figsize=(8, 8))
      plt.pie(pollutants_mean_values, labels=pollutants_mean_values.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
      plt.title('Average Pollutant Concentrations Percentage')
      plt.show()
      st.pyplot(plt.gcf())

      with tab3:
        for item in pollutants:
          plt.figure(figsize=(12, 6))
          plt.hist(combined_dataFrame[item], bins=30, edgecolor='black', alpha=0.7)
          plt.xlabel(item + ' Concentration (ug/m3)')
          plt.ylabel('Frequency')
          plt.title(f'Overall Hourly Distribution of {item} Concentration')
          plt.show()
          st.pyplot(plt.gcf())


