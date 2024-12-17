import pandas as pd
import streamlit as st
import main
import preprocessing
import EDA
import modeling

st.title("Beijing Multi-Site Air Quality Data Analysis")
combined_dataFrame = None
csv_file = st.file_uploader("Please Upload the CSV file to start the analysis", type='csv')

if csv_file is not None:
    combined_dataFrame = pd.read_csv(csv_file)

    st.sidebar.title("AQI Application")
    page = st.sidebar.radio("Select a page please:", ["Data Overview", "Exploratory Data Analysis (Part1)", "Exploratory Data Analysis (Part2)", "Modelling and Prediction"])
    
    if page == "Data Overview":
        main.Data_Overview(combined_dataFrame)
    elif page == "Exploratory Data Analysis (Part1)":
        preprocessing.EDA_Part1(combined_dataFrame)
    elif page == "Exploratory Data Analysis (Part2)":
        EDA.EDA_Part2(combined_dataFrame)
    elif page == "Modelling and Prediction":
        modeling.modeling_prediction(combined_dataFrame)
else:
    st.warning("Please upload a CSV file to start the analysis")
