import streamlit as st
import pandas
from pydataset import data


st.title ('Pydataset')

selected_data = st.sidebar.selectbox('Select a dataset', data().dataset_id)


st.header('Datasets')
st.subheader(' List of Dataset')
with st.expander ('show list of dataset'):
    st.write(data())

st.subheader (f'Selected data (`{selected_data}`)')
st.write(data(selected_data))