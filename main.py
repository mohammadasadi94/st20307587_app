import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def Data_Overview(combined_dataFrame):
  st.header("General insight about the data")
  information=['Number of rows and columns','Data types','Data Overview','Basic Statistics','Number of missing values']
  selected_info = st.multiselect('What information would you like to see about the data?',information,default=information[:1])

  if 'Number of rows and columns' in selected_info:
    st.subheader('Number of rows and columns')
    st.write(combined_dataFrame.shape)

  if 'Data types' in selected_info:
    st.subheader('Data types')
    st.write(combined_dataFrame.dtypes)

  if 'Data Overview' in selected_info:
    st.subheader("Data Overview")
    st.write(combined_dataFrame.head(10))
  if 'Basic Statistics' in selected_info:
    st.subheader('Basic Statistics')
    st.write(combined_dataFrame.describe())

  if 'Number of missing values' in selected_info:
    st.subheader('Number of missing values')
    st.write(combined_dataFrame.isnull().sum())