def modeling_prediction(combined_dataFrame):
  from sklearn.model_selection import train_test_split
  from sklearn.linear_model import LinearRegression
  from sklearn.neighbors import KNeighborsRegressor
  from sklearn.tree import DecisionTreeRegressor
  from sklearn.metrics import r2_score
  from sklearn.preprocessing import StandardScaler
  import numpy as np
  import streamlit as st
  import matplotlib.pyplot as plt

  columns=['PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','WSPM','wd','WSPM']
  for item in columns:
    combined_dataFrame[item] = combined_dataFrame[item].ffill()


  Target_pollutant = ['PM10', 'SO2', 'NO2', 'CO', 'O3','PM2.5']
  option = st.selectbox('Choose a pollutant you would like to predict:',['PM2.5','PM10','CO', 'NO2', 'O3','SO2'])
  if option == 'PM2.5':
    X_LR = combined_dataFrame[['PM10','SO2','NO2','CO','TEMP','WSPM']]
    y_LR = combined_dataFrame[['PM2.5']]
    X_KNN = combined_dataFrame[['PM10','SO2','NO2','CO','TEMP','WSPM']]
    y_KNN = combined_dataFrame[['PM2.5']]
    X_DT = combined_dataFrame[['PM10','SO2','NO2','CO','TEMP','WSPM']]
    y_DT = combined_dataFrame[['PM2.5']]
    n_neighbors=14
    weights='distance'

  elif option == 'PM10':
    X_LR = combined_dataFrame[['PM2.5', 'SO2', 'NO2', 'CO', 'TEMP']]
    y_LR = combined_dataFrame[['PM10']]
    X_KNN = combined_dataFrame[['PM2.5', 'SO2', 'NO2', 'CO', 'TEMP']]
    y_KNN = combined_dataFrame[['PM10']]
    X_DT = combined_dataFrame[['PM2.5', 'SO2', 'NO2', 'CO', 'TEMP']]
    y_DT = combined_dataFrame[['PM10']]
    n_neighbors=15
    weights='distance'

  elif option == 'CO':
    X_LR = combined_dataFrame[['PM2.5', 'PM10','NO2', 'TEMP']]
    y_LR = combined_dataFrame[['CO']]
    X_KNN = combined_dataFrame[['PM2.5', 'PM10','NO2', 'TEMP']]
    y_KNN = combined_dataFrame[['CO']]
    X_DT = combined_dataFrame[['PM2.5', 'PM10','NO2', 'TEMP']]
    y_DT = combined_dataFrame[['CO']]
    n_neighbors=15
    weights='distance'

  elif option == 'NO2':
    X_LR = combined_dataFrame[['PM2.5', 'PM10', 'CO', 'TEMP']]
    y_LR = combined_dataFrame[['NO2']]
    X_KNN = combined_dataFrame[['PM2.5', 'PM10', 'CO', 'TEMP']]
    y_KNN = combined_dataFrame[['NO2']]
    X_DT = combined_dataFrame[['PM2.5', 'PM10', 'CO', 'TEMP']]
    y_DT = combined_dataFrame[['NO2']]
    n_neighbors= 15
    weights='uniform'

  elif option == 'O3':
    X_LR = X = combined_dataFrame[['TEMP', 'DEWP', 'RAIN']]
    y_LR = combined_dataFrame[['O3']]
    X_KNN = X = combined_dataFrame[['TEMP', 'DEWP', 'RAIN']]
    y_KNN = combined_dataFrame[['O3']]
    X_DT = X = combined_dataFrame[['TEMP', 'DEWP', 'RAIN']]
    y_DT = combined_dataFrame[['O3']]
    n_neighbors=15
    weights='uniform'

  elif option == 'SO2':
    X_LR = combined_dataFrame[['PM2.5', 'PM10', 'NO2', 'CO']]
    y_LR = combined_dataFrame[['SO2']]
    X_KNN = combined_dataFrame[['PM2.5', 'PM10', 'NO2', 'CO']]
    y_KNN = combined_dataFrame[['SO2']]
    X_DT = combined_dataFrame[['PM2.5', 'PM10', 'NO2', 'CO']]
    y_DT = combined_dataFrame[['SO2']]
    n_neighbors=15
    weights='distance'


  X_LR_train, X_LR_test, y_LR_train, y_LR_test = train_test_split(X_LR, y_LR, test_size=0.20,random_state=42)
  regr = LinearRegression()
  regr.fit(X_LR_train,y_LR_train)
  y_LR_prediction =  regr.predict(X_LR_test)


  X_KNN_train, X_KNN_test, y_KNN_train, y_KNN_test = train_test_split(X_KNN, y_KNN, test_size=0.20, random_state=42)

  scaler_KNN = StandardScaler()
  X_KNN_train_scaled = scaler_KNN.fit_transform(X_KNN_train)
  X_KNN_test_scaled = scaler_KNN.transform(X_KNN_test)

  KNN = KNeighborsRegressor(n_neighbors=n_neighbors, weights=weights)
  KNN.fit(X_KNN_train_scaled, y_KNN_train)
  y_KNN_prediction = KNN.predict(X_KNN_test_scaled)

  X_DT_train, X_DT_test, y_DT_train, y_DT_test = train_test_split(X_DT, y_DT, test_size=0.20, random_state=42)
  scaler_DT = StandardScaler()
  X_DT_train_scaled = scaler_DT.fit_transform(X_DT_train)
  X_DT_test_scaled = scaler_DT.transform(X_DT_test)
  regressor = DecisionTreeRegressor(criterion='squared_error', random_state=42, max_depth=10)
  regressor.fit(X_DT_train_scaled, y_DT_train)
  y_DT_prediction = regressor.predict(X_DT_test_scaled)



  tab1, tab2, tab3,tab4 = st.tabs(["Linear Regression Model","KNN Model","Decision Tree Model","Model Accuracy Comparison (R2)"])
  with tab1:
    st.header("Linear Regression Model")
    st.write("Mean absolute error: %.2f" % np.mean(np.absolute(y_LR_prediction-y_LR_test)))
    st.write("Residual sum of squares (MSE): %.2f" % np.mean((y_LR_prediction-y_LR_test)**2))
    st.write("R2-score: %.2f" % r2_score(y_LR_prediction,y_LR_test))
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(y_LR_test)), y_LR_test, color='blue', label='Actual Data')
    plt.scatter(range(len(y_LR_prediction)), y_LR_prediction, color='red', label='Predicted Data', alpha=0.7)
    plt.xlabel('Sample Index')
    plt.ylabel('PM2.5 (ug/m³)')
    plt.title(f'Actual vs Predicted values for the {option} pollutant')
    plt.legend()
    plt.show()
    st.pyplot(plt.gcf())
  with tab2:
    st.header("KNN Model")
    st.write("Mean absolute error: %.2f" % np.mean(np.absolute(y_KNN_prediction-y_KNN_test)))
    st.write("Residual sum of squares (MSE): %.2f" % np.mean((y_KNN_prediction-y_KNN_test)**2))
    st.write("R2-score: %.2f" % r2_score(y_KNN_prediction,y_KNN_test))
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(y_KNN_test)), y_KNN_test, color='blue', label='Actual Data')
    plt.scatter(range(len(y_KNN_prediction)), y_KNN_prediction, color='red', label='Predicted Data', alpha=0.7)
    plt.xlabel('Sample Index')
    plt.ylabel('PM2.5 (ug/m³)')
    plt.title(f'Actual vs Predicted values for the {option} pollutant')
    plt.legend()
    plt.show()
    st.pyplot(plt.gcf())
  with tab3:
    st.header("Decision Tree Model")
    y_DT_test = y_DT_test.values.ravel()
    st.write("Mean absolute error: %.2f" % np.mean(np.absolute(y_DT_prediction-y_DT_test)))
    st.write("Residual sum of squares (MSE): %.2f" % np.mean((y_DT_prediction-y_DT_test)**2))
    st.write("R2-score: %.2f" % r2_score(y_DT_prediction,y_DT_test))
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(y_DT_test)), y_DT_test, color='blue', label='Actual Data')
    plt.scatter(range(len(y_DT_prediction)), y_DT_prediction, color='red', label='Predicted Data', alpha=0.7)
    plt.xlabel('Sample Index')
    plt.ylabel('PM2.5 (ug/m³)')
    plt.title(f'Actual vs Predicted values for the {option} pollutant')
    plt.legend()
    plt.show()
    st.pyplot(plt.gcf())
  with tab4:
    st.header("Model Accuracy Comparison (R2)")
    plt.figure(figsize=(10, 6))
    models = ['Linear Regression', 'KNN', 'Decision Tree']
    r2_scores = [r2_score(y_LR_prediction,y_LR_test), r2_score(y_KNN_prediction,y_KNN_test), r2_score(y_DT_prediction,y_DT_test)]
    plt.bar(models, r2_scores)
    plt.xlabel('Models')
    plt.ylabel('R2 Score')
    plt.title('Model Accuracy Comparison')
    plt.show()
    st.pyplot(plt.gcf())









