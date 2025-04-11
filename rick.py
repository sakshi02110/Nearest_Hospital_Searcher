import streamlit as st
from matplotlib import image
import os
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from pathlib import Path
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="hospital_locator")

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# # absolute path to this file
# FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# # absolute path to this file's root directory
# PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
# # absolute path of directory_of_interest
# dir_of_interest = os.path.join(PARENT_DIR, "resources")
#
# # data_path = os.path.join(dir_of_interest, "data", "Cleaned_Hospital.csv")
# #
# # df = pd.read_csv(data_path)
# IMAGE_PATH = os.path.join(dir_of_interest, "images", "hospital.png")
# # Image section of Laptop

# directory of the files and images
cur_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
IMAGE_PATH = cur_dir / "assets" / "hospital.png"
data_path = cur_dir / "resources" / "data" /"Cleaned_Hospital.csv"


st.set_page_config(page_title=" Hospital",
                   page_icon="🏥",
                   layout="wide"
)

# st.markdown("<h1 style='text-align: center; color: Yellow;'>🤖  👨‍⚕️</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>📌 Hospital Near You 🗺️</h1>", unsafe_allow_html=True)


# page_bg_img = '''

# Place this near the top of your script (after imports and before any Streamlit code):
bg_img_base64 = get_base64_image("assets/medicine-5.webp")

page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/webp;base64,{bg_img_base64}");
    background-size: cover;
    background-attachment: fixed;
    background-position: top center;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

img = image.imread(IMAGE_PATH)

# <style>
# .stApp {
# background-image: images/medicine-5.webp;
# # background-image: url("https://e1.pxfuel.com/desktop-wallpaper/142/164/desktop-wallpaper-chatbots-in-healthcare-more-than-basic-user-queries-chatbot.jpg");
# background-size: cover;
# background-position: top center;
# }
# </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)
# img = image.imread(IMAGE_PATH)


df = pd.read_csv(data_path)


col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.image(img, width=400, caption="Keep Calm!!! Believe in US")

with col3:
    st.write(' ')

st.markdown("<h2 style='text-align: center; color: black;'>🧑‍💻 The Input Section 👩‍💻</h2>", unsafe_allow_html=True)
error_msg1 = f"Latitude value must be between 19.445685 and 28.256987."
# lat = st.number_input("Enter Your Latitude:", value=df.latitude.mean(), min_value=19.445685, max_value=28.256987, step=0.000001, format="%.6f")
# with st.form("city_form"):
#     city_name = st.text_input("🏙️ Enter City:")
#     submitted = st.form_submit_button("🔍 Locate")
# Add this CSS styling block before the form
# Centered and styled city input form
import streamlit as st

# Add custom CSS for centering and styling
st.markdown("""
    <style>
        .form-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .form-box {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
            width: 50%;
            max-width: 200px;
        }

        input[type="text"] {
            width: 50px
            font-size: 70px;
            padding: 10px;
            font-weight: bold;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        button[kind="primary"] {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Start your container
# st.markdown('<div class="form-container"><div class="form-box">', unsafe_allow_html=True)

# Actual form
with st.form("city_form"):
    city_name = st.text_input("🌐 Enter the name of the City:")
    submitted = st.form_submit_button("🔍 Locate")

    if submitted:
        st.success(f"Showing results for: **{city_name}**")

# Close divs
st.markdown('</div></div>', unsafe_allow_html=True)



# city_name = st.text_input("Enter Your City Name (e.g., Kolkata, Siliguri):")
if city_name:
    location = geolocator.geocode(city_name)
    if location:
        lat = location.latitude
        long = location.longitude
        st.success(f"📍 Located city '{city_name}' at (Lat: {lat}, Lon: {long})")

        # Now safely use lat & long
        if not 19.445685 <= lat <= 28.256987:
            st.error("Latitude value must be between 19.445685 and 28.256987.")
        elif not 85.126002 <= long <= 90.235698:
            st.error("Longitude value must be between 85.126002 and 90.235698.")
        else:
            ans = np.array((lat, long))
            arr = np.transpose(np.array([df.latitude, df.longitude]))
            dis = np.sqrt(np.sum((arr - ans) ** 2, axis=1))
            newdis = [round(i, 4) for i in dis]
            df["Distance"] = newdis
            top_5_hos = df.sort_values(by='Distance').head(num)

            butt = st.button("Tap & Be Cured 🏥")
            if butt:
                # your map + hospital card rendering logic here
                ...
    else:
        st.error("❌ Could not find the location. Please enter a valid city name.")

# if city_name:
#     location = geolocator.geocode(city_name)
#     if location:
#         lat = location.latitude
#         long = location.longitude
#         st.success(f"📍 Located city '{city_name}' at (Lat: {lat}, Lon: {long})")
#     else:
#         st.error("❌ Could not find the location. Please enter a valid city name.")
# ans = np.array((lat, long))
# arr = np.transpose(np.array([df.latitude, df.longitude]))
# dis = np.sqrt(np.sum((arr-ans)**2, axis=1))
# ...

# if city_name:
#     location = geolocator.geocode(city_name)
#     if location:
#         lat = location.latitude
#         long = location.longitude
#         st.success(f"📍 Located city '{city_name}' at (Lat: {lat}, Lon: {long})")
#     else:
#         st.error("❌ Could not find the location. Please enter a valid city name.")
# ans = np.array((lat, long))
# arr = np.transpose(np.array([df.latitude, df.longitude]))
# dis = np.sqrt(np.sum((arr-ans)**2, axis=1))
# ...

# if not 19.445685 <= lat <= 28.256987:
#     st.error(error_msg1)
# error_msg2 = f"Longitude value must be between 85.126002 and 90.235698."
# # long = st.number_input("Enter Your Longitude:", value=df.longitude.mean(), min_value=85.126002, max_value=90.235698, step=0.000001, format="%.6f")

# if not 85.126002 <= long <= 90.235698:
#     st.error(error_msg2)

num = st.slider("Enter the no of Nearest Hospital you want:", 2, 10, 5)

# st.markdown("<b><h2 style='text-align: center; color: black;'>1) After entering the values please press the Enter ⎆ key 🤔</h2></b>", unsafe_allow_html=True)
# st.markdown("<b><h2 style='text-align: center; color: black;'>2) If Error occured i.e. the value is beyond of the renge then please currect that before entering further, this is because "
#             "we are predicting that you are near about West Bengal as the data is restricted to WB 🥺🥺</h2></b>", unsafe_allow_html=True)


ans = np.array((lat, long))

arr = np.transpose(np.array([df.latitude, df.longitude]))

dis = np.sqrt(np.sum((arr-ans)**2, axis=1))

dis = dis.tolist()

newdis = [round(i, 4) for i in dis]

df["Distance"] = newdis

top_5_hos = df.sort_values(by='Distance').head(num)

butt = st.button("Tap & Be Cured 🏥")
if butt:
    st.markdown("<h3 style='text-align: center; color: black;'>We found {} Nearest Hospital for you </h3>".format(num),
                unsafe_allow_html=True)

    rg = top_5_hos[['Name Of Hospital', 'Address of Hospital',
       'current address', 'Phone Number', 'Class Recommended', 'latitude',
       'longitude']]
    st.dataframe(rg)
    st.markdown(
        "<h6 style='text-align: left; color: black;'>Double tap on any cell for more info</h6>",
        unsafe_allow_html=True)

    m = folium.Map(location=[lat, long], zoom_start=13)
    folium.Marker(location=[lat, long], icon=folium.Icon(icon='home', color='red', prefix="fa"), popup='Your Location',
                  size=155).add_to(m)

    for index, row in top_5_hos.iterrows():
        # Extract the hospital details from the row
        hospital_location = [row['latitude'], row['longitude']]
        hospital_name = row['Name Of Hospital']
        hospital_address = row['current address']
        hospital_phone = row['Phone Number']
        class_rec = row["Class Recommended"]

        # hovering to show the name of hospital

        #     tooltip_text = f"{hospital_name}"
        #     tooltip = folium.Tooltip(f"{hospital_name}")

        # Create a marker for the hospital
        popup_text = f"<b>{hospital_name}</b><br>{hospital_address}<br>Phone: {hospital_phone}<br>{class_rec}"
        folium.Marker(
            tooltip=str(df.iloc[index]['Name Of Hospital']),
            location=hospital_location,
            popup=popup_text,
            icon=folium.Icon(icon='medkit', prefix='fa', color='red')
        ).add_to(m)

    # make the map at middle

    col4, col5, col6 = st.columns(3)
    with col4:
        st.write(' ')

    with col5:
        folium_static(m)


    with col6:
        st.write(' ')


    st.markdown(
        "<h5 style = 'color: black;'> 1) Squeeze/zoom out the map to view the all of your nearest hospitals</h5>",
        unsafe_allow_html=True)
    st.markdown(
        "<h5 style = 'color: black;'> 2) Tap on the pin to view the info regarding the hospitals and its address</h5>",
        unsafe_allow_html=True)
    st.markdown(
        "<b><h5 style = 'color: black;'>3) There are too few datas in the dataset of 250 entries</h5></b>",
        unsafe_allow_html=True)

    st.markdown(
                "<b><h3 style='text-align: center; color: black;'> Hope You Enjoyed 😊</h3></b>",
                 unsafe_allow_html=True)


# st.subheader("After Completion, Move back to the previous tab of and complete your conversation 🆓")




