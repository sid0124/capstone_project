import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analysis App")
# Load dataset
new_df = pd.read_csv('dataset/data_viz1.csv')
feature_text = pickle.load(open('dataset/feature_text.pkl','rb'))

# Convert necessary columns to numeric (forcing errors='coerce' will turn invalid values into NaN)
numeric_columns = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
new_df[numeric_columns] = new_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Group by 'sector' and compute the mean
group_df = new_df.groupby('sector')[numeric_columns].mean()

st.header('Sector price per Sqft Geomap')
fig = px.scatter_mapbox(group_df,lat='latitude',lon='longitude',color= 'price_per_sqft',size='built_up_area',color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index )
st.plotly_chart(fig,use_container_width=True)

st.header('Feature Cloud')

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='black',
                      stopwords ={'s'},  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

plt.figure(figsize=(8,8),facecolor=None)
fig, ax = plt.subplots()
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
st.pyplot(fig)

st.header('Area VS Price')
property_type=st.selectbox('Select property type',['flat','house'])

if property_type == "house":
    fig1 = px.scatter(new_df[new_df['property_type']=='house'],x='built_up_area',y='price',color='bedRoom',title='Area VS Price')
    st.plotly_chart(fig1, use_container_width=True)

if property_type == 'flat':
    fig1 = px.scatter(new_df[new_df['property_type']=='flat'],x='built_up_area',y='price',color='bedRoom',title='Area VS Price')
    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')
select_sector = st.selectbox('Select Sector',sector_options)

if select_sector == 'overall':
    fig2 = px.pie(new_df,names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

else:
    fig2 = px.pie(new_df[new_df['sector']== select_sector],names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK Price comparison')
fig3 = px.box(new_df[new_df['bedRoom']<=4],x = 'bedRoom',y = 'price',title = 'BHK Price comparison')
st.plotly_chart(fig3, use_container_width=True)

st.header('Side by Side Distplot for property type')
fig4 = plt.figure(figsize=(10,4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig4)
