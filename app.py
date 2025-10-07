import streamlit as st
from apputil import Genius
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file
token = os.getenv("ACCESS_TOKEN")  # fetches the Genius token


st.write(
'''
# Week x: Genius API Exercise

...
'''
)

# keep the exercise input from skeleton
amount = st.number_input("Exercise Input: ", 
                         value=None, 
                         step=1, 
                         format="%d")

if amount is not None:
    st.write(f"The exercise input was {amount}.")

# --- Genius API Exercises ---

# Step 1: API Token input
token = os.getenv("ACCESS_TOKEN")
if not token:
    st.warning(" No token found in .env file.")
else:
    st.success(" Genius token loaded from .env file")
    genius = Genius(access_token=token)

    # --- Exercise 1/2: Single Artist ---
    st.subheader("Exercise 1 & 2: Single Artist Info")

    artist_name = st.text_input("Enter an artist name (e.g., Radiohead):")

    if artist_name:
        try:
            artist_data = genius.get_artist(artist_name)
            st.write(f"Showing data for **{artist_name}**:")
            st.json(artist_data)   # pretty print JSON
        except Exception as e:
            st.error(str(e))

    # --- Exercise 3: Multiple Artists ---
    st.subheader("Exercise 3: Multiple Artists Info")

    artist_list_input = st.text_area("Enter multiple artist names (comma separated, e.g. Rihanna, Tycho, Seal, U2):")

    if artist_list_input:
        terms = [t.strip() for t in artist_list_input.split(",") if t.strip()]
        if terms:
            try:
                df = genius.get_artists(terms)
                st.write("Artists DataFrame:")
                st.dataframe(df)   # display nice table
            except Exception as e:
                st.error(str(e))
