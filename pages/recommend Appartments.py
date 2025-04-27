import streamlit as st
import pickle
import pandas as pd
import numpy as np
from streamlit import button

st.set_page_config(page_title="Recommend Apartments")

location_df = pd.read_pickle('dataset/location_distance.pkl')

cosine_sim1 = pickle.load(open('dataset/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('dataset/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('dataset/cosine_sim3.pkl','rb'))

def recommend_property_with_scores(property_name,top_n=5):
    cosine_sim_matrix = 0.5*cosine_sim1+ 0.8*cosine_sim2+ 1*cosine_sim3

    sim_score = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    sorted_score = sorted(sim_score ,key = lambda x : x[1],reverse=True)

    top_indices = [i[0] for i in sorted_score[1:top_n+1]]
    top_scores  = [i[1] for i in sorted_score[1:top_n+1]]

    top_properties = location_df.index[top_indices].to_list()

    recommendation_df = pd.DataFrame({
        'Property_name' : top_properties,
        'Similarity_score' : top_scores
    })

    return recommendation_df

recommend_property_with_scores('DLF The Camellias')

st.title('Select the Location and Radius')

select_location = st.selectbox('Location',location_df.columns.to_list())

Radius = st.number_input("Radius in Kms")

if st.button("Search"):
    result_ser = location_df[location_df[select_location]<=Radius*1000][select_location].sort_values()

    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) +'kms')

st.title('Recommends Apartments')
select_apartment = st.selectbox('Select an Apartment', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommend_df = recommend_property_with_scores(select_apartment)

    st.dataframe(recommend_df)








