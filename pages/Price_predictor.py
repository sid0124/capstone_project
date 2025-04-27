import streamlit as st
import pickle
import pandas as pd
import numpy as np
import py7zr
import os

st.set_page_config(page_title="Price Predictor")

# --- Load df.pkl ---
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)


archive_path = 'pipeline.pkl.7z'
extract_path = 'pkl_file'

if not os.path.exists(extract_path):
    os.makedirs(extract_path)


if not os.path.exists(os.path.join(extract_path, 'pipeline.pkl')):
    with py7zr.SevenZipFile(archive_path, mode='r') as z:
        z.extractall(path=extract_path)


with open(os.path.join(extract_path, 'pipeline.pkl'), 'rb') as file:
    pipeline = pickle.load(file)


st.header('Enter your inputs')

property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox('Sector', sorted(df['sector'].dropna().astype(str).unique().tolist()))
Bedroom = float(st.selectbox('No. of bedroom', sorted(df['bedRoom'].unique().tolist())))
bathroom = float(st.selectbox('No. of bathroom', sorted(df['bathroom'].unique().tolist())))
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
built_up_area = float(st.number_input('Built Up Area'))
servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):
    data = [[
        property_type, sector, Bedroom, bathroom, balcony,
        property_age, built_up_area, servant_room, store_room,
        furnishing_type, luxury_category, floor_category
    ]]

    columns = [
        'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
        'agePossession', 'built_up_area', 'servant room', 'store room',
        'furnishing_type', 'luxury_category', 'floor_category'
    ]

    one_df = pd.DataFrame(data, columns=columns)

    base_line = np.expm1(pipeline.predict(one_df))[0]
    low_price = base_line - 0.22
    high_price = base_line + 0.22

    st.success("The price of the flat is between {} Cr and {} Cr".format(round(low_price, 2), round(high_price, 2)))
