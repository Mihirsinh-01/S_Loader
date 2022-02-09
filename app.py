import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine
from PIL import Image
import pymysql
import plotly.graph_objects as go

#Title
st.title("Welcome to S-Loader")
image = Image.open('logos.png')
st.image(image,caption='Team Members: Prakhar Awasthi (PM), Harsh Panchal (SWE), Lekesh Kumar (DE), Mihirsinh Vaja (SWE), Rushil Bangia (CE), Sonali Patil (SWE)')

#To Upload Excel File 
uploaded_files = st.file_uploader("Choose any Excel file",type=['xls','xlsx'], accept_multiple_files=True)

#Limit Excel File to 5 and display data
if len(uploaded_files) > 5:
  st.error("Maximum 5 files allowed")
else:
  names=[]

  # Database Connection
  conn=create_engine("mysql+pymysql://sql6471133:beqfXgcLEM@sql6.freesqldatabase.com/sql6471133")
  
  for uploaded_file in uploaded_files:
    names.append(uploaded_file.name)
    st.write("Uploaded Filename:", uploaded_file.name)
    dataframe = pd.read_excel(uploaded_file)
    # Inserting Dataframe directly to MySQL server.
    dataframe.to_sql(con=conn,name=uploaded_file.name.split(".")[0],if_exists="replace")
    st.write(dataframe)

  if names:
    st.sidebar.title('DATA FILTERS')
    option = st.sidebar.selectbox('What would you like to view?', names)
    st.write('You selected:', option)
    selected_file=""
    for x in uploaded_files:
      if x.name==option:
        selected_file=x
        break
    df=pd.read_excel(selected_file)
    #df.drop("<NA>", axis=1, inplace=True)
    cols=df.columns.values.tolist()
    att=st.sidebar.selectbox("Select the attribute .. ", cols)
    data=df[att]
    freq={}
    for x in data:
      if x in freq:
        freq[x]+=1
      else:
        freq[x]=1

    fig = go.Figure(
    go.Pie(
    labels = list(freq.keys()),
    values = list(freq.values()),
    hoverinfo = "label+percent",
    textinfo = "percent"))

    st.header("Pie chart for "+att)
    st.plotly_chart(fig)
    
    
    #query = f"selected_file=='{cols}'"
    #df_filtered = df.query(query)
    
    #if st.checkbox("Show Summary of Dataset"):    
    
    st.area_chart(cols)
  
    #X = st.sidebar.multiselect('Choose position:', positions, default=positions)