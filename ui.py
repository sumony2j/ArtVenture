import streamlit as st
from PIL import Image, ImageFilter
import cv2
import os
import numpy as np
from function import *
import sqlite3

def create_table():
    conn = sqlite3.connect('./Database/feedback.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS FEEDBACK (NAME VARCHAR, EMAIL VARCHAR, RATING NUMBER, FEEDBACK VARCHAR)")
    conn.commit()
    conn.close()

def insert_data(name,email,rating,feedback):
    conn = sqlite3.connect('./Database/feedback.db')
    cursor = conn.cursor()
    query = f"INSERT INTO FEEDBACK VALUES('{name}','{email}','{rating}','{feedback}')"
    cursor.execute(query)
    conn.commit()
    conn.close()


c1,c2 = st.columns(2)
st.sidebar.header("ArtVenture")

uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    image.save("./save_img.jpg")

filter_type = st.sidebar.radio(
    "Select a filter type",
    ("Black&White","Bright","Sharp","Sepia","High Dynamic","Invert","Blur","Paint","Sketch","Cartoon","Texture")
)

if uploaded_image is not None:
    if filter_type == "Sketch":
        slider = st.sidebar.slider('Adjust the intensity', 9, 501, step=2)
        filtered_image = sketch("./save_img.jpg",slider)
    elif filter_type == "Cartoon":
        filtered_image = cartoon("./save_img.jpg")
    elif filter_type == "Sepia":
        filtered_image = sepia("./save_img.jpg")
    elif filter_type == "Sharp":
        filtered_image = sharp("./save_img.jpg")
    elif filter_type == "Invert":
        filtered_image = invert("./save_img.jpg")
    elif filter_type == "Black&White":
        filtered_image = greyscale("./save_img.jpg")
    elif filter_type == "Blur":
        slider = st.sidebar.slider('Adjust the intensity', 9, 501, step=2)
        filtered_image = blur("./save_img.jpg",slider)
    elif filter_type == "Paint":
        slider_s = st.sidebar.slider('Adjust the smoothness', 2, 200, step=1)
        slider_r = st.sidebar.slider('Adjust the edges', 0.0, 1.0, step=0.1)
        filtered_image = style("./save_img.jpg",slider_s,slider_r)
    elif filter_type == "Texture":
        slider_s = st.sidebar.slider('Adjust the smoothness', 2, 200, step=1)
        slider_r = st.sidebar.slider('Adjust the edges', 0.0, 1.0, step=0.1)
        filtered_image = textured("./save_img.jpg",slider_s,slider_r)
    elif filter_type == "Bright":
        slider = st.sidebar.slider('Adjust the intensity', -200, 501, step=1)
        filtered_image = bright("./save_img.jpg",slider)
    elif filter_type == "High Dynamic":
        slider_s = st.sidebar.slider('Adjust the smoothness', 2, 200, step=1)
        slider_r = st.sidebar.slider('Adjust the edges', 0.0, 1.0, step=0.1)
        filtered_image = HDR("./save_img.jpg",slider_s,slider_r)

    with c1:
        st.image(image, caption="Original Image", use_column_width=True)
    with c2:
        st.image(filtered_image, caption=f"{filter_type} Image", use_column_width=True)
        os.remove("./save_img.jpg")

#Add a feedback section in the sidebar
st.sidebar.title('FeedBack') #Used to create some space between the filter widget and the comments section
st.sidebar.subheader('Please help us improve!')
with st.sidebar.form(key='columns_in_form',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
    name=st.text_input(label='Enter your name')
    email=st.text_input(label='Enter your email')
    rating=st.slider("Please rate the app", min_value=1, max_value=5, value=3,help='Drag the slider to rate the app. This is a 1-5 rating scale where 5 is the highest rating')
    text=st.text_input(label='Please leave your feedback here')
    submitted = st.form_submit_button('Submit')
    if submitted:
      create_table()
      insert_data(name,email,rating,text)
      st.write('Thanks for your feedback!')
      st.markdown('Your Rating:')
      st.markdown(rating)
      st.markdown('Your Feedback:')
      st.markdown(text)


