import pyshorteners
import streamlit as st

def url_shortener(url):
    shortener = pyshorteners.Shortener()
    shorted_url = shortener.tinyurl.short(url)
    return shorted_url

# AppWeb con Streamlit
st.set_page_config(page_title="URL Shortener", page_icon="./resources/favicon.ico",  layout="centered")
st.image("./resources/logohorizontal.png", use_column_width=True)
st.title("URL Shortener")
url = st.text_input("Enter the Original URL:")
if st.button("Generete new URL"):
    st.write("Shortened URL: ", url_shortener(url))