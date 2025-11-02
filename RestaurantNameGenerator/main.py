import streamlit as st
import json
from langchain_helper import generate_restaurant_name_and_items

st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian","Italian","Mexian","Japanese"))

if cuisine:
    response = generate_restaurant_name_and_items(cuisine)
    st.header(response['restaurant_name'].strip().strip('"').strip("'"))
    menu_items = json.loads(response['menu_items'])
    st.write("**Menu Items**")
    for i,item in enumerate(menu_items,1):
        st.write(f"{i}. {item}")