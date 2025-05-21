import streamlit as st

st.title("first streamlit app")
st.header("my first streamlit app")
st.text("this is a simple streamlit app")
st.code("print('hello world')", language='python')

import pandas as pd
df=pd.read_csv("retail_sales_data.csv")

df['Date']=pd.to_datetime(df['Date'])
st.dataframe(df)

st.bar_chart(data=df,x="Date" ,y="Total Amount",use_container_width=True)