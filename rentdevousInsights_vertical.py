# Core packages
import streamlit as st

# Additional packages
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import shape
import matplotlib.pyplot as plt

# Import functions from backend.py
from backend import filter_neighborhood_group
from backend import NY_staging
from backend import filter_price
from backend import HW_staging
from backend import mongo_connect
from backend import get_neighborhoods

# Declare variables to be used on the page
# Dropdown list for New York
NY_Boroughs = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]

# Dropdown list options for Hawaii
HI_Boroughs = ["Maui", "Honolulu", "Kauai", "Hawaii"]

st.set_page_config(
    page_title="Welcome to Insights for Potential Rentdevous Hosts by APAN 5400 Group 5",
    page_icon="images/logoico.ico",
    layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=["Home", "New York", "Hawaii", "New Jersey", "Georgia", "Dev Stack/Team", "Contact Us"],
        icons=["file-earmark", "house-check", "house-check", "house-x", "house-x", "person-lines-fill", "info-square"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#000000"},
            "icon": {"font-size": "18px", "color": "white"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "Gray"},
            "nav-link-selected": {"background-color": "brown"}
        }
    )

if selected == "Home":
    st.image("images/header.svg", width=300)
    st.title("Insights for Potential Rentdevous Hosts")
    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)
    st.write(""":gray[Rentdevous hosts face challenges in optimizing their listings due to a lack of 
    comprehensive market insights. The competitive landscape of RentIt hosting and the challenges in optimising 
    listings for higher revenue and guest satisfaction have been a major concern for hosts. This solution enables
    Rentdevous hosts make data-driven decisions to enhance their listings' competitiveness and profitability 
    through targeted analytics and insights. This pilot run covers the states of New York and Hawaii while 
    New Jersey and Georgia will be rolling out soon. Please explore the site through the menu options at the top and 
    feel free to drop a feedback.]
    """)
    # Display background images
    st.image("images/housing9.png")
    st.image("images/housing13.png")
    st.image("images/housing15.png")
    st.image("images/housing11.png")

if selected == "New York":
    st.title("Search in New York")
    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)

    # Fetch options for the Borough dropdown list
    NY_Borough = st.selectbox("Select a Borough", NY_Boroughs)

    # Fetch options for the Neighborhood dropdown list
    NY_Neighborhood_Areas = get_neighborhoods(NY_Borough)
    NY_Neighborhood_Area = st.selectbox('Select a Neighborhood', NY_Neighborhood_Areas)

    # Get listings for the Borough selected
    filtered_NYC_hood = filter_neighborhood_group(NY_staging, NY_Borough)

    upper_range_NY = int(max(tup[10] for tup in filtered_NYC_hood))

    # Add a slider for minimum and maximum price
    min_price, max_price = st.slider("Price Range ($)", 1, upper_range_NY, (1, upper_range_NY))

    # Filter data based on price range
    filtered_NYC_price = filter_price(filtered_NYC_hood, min_price, max_price)

    if st.button("Search"):
        if len(filtered_NYC_price) > 0:
            # Display the count of results for the slider
            filtered_count_NY = len(pd.DataFrame(filtered_NYC_price))
            st.success(f"{filtered_count_NY} listings were fetched for {NY_Borough}.")

            # Extract longitude (index 4) and latitude (index 5)
            latitude_NY = [item[4] for item in filtered_NYC_price]
            longitude_NY = [item[5] for item in filtered_NYC_price]
            neighborhood_NY = [item[14] for item in filtered_NYC_price]

            # Create a DataFrame with lat and lon columns
            filtered_map_data_NY = pd.DataFrame(
                {'lat': latitude_NY, 'lon': longitude_NY, 'neighborhood_area': neighborhood_NY})

            # Create a scatter map using Plotly Express
            fig_NY = px.scatter_mapbox(
                filtered_map_data_NY,
                lat="lat",  # Replace with your actual column name for latitude
                lon="lon",  # Replace with your actual column name for longitude
                title=f"Neighborhoods in {NY_Borough}",
                hover_name="neighborhood_area",  # Customize hover information
                zoom=10,  # Adjust the initial zoom level
                color_discrete_sequence=["red"],
                opacity=0.9,  # Adjust marker opacity
                size_max=15,  # Adjust marker size
                width=876,
                height=800,
                mapbox_style="carto-positron",
                # Custom marker settings
                custom_data=['lat', 'lon', 'neighborhood_area']
            )

            # # Display the map
            st.plotly_chart(fig_NY)

            # Display the second map

            highlight_neighbourhood = NY_Neighborhood_Area
            highlight_group = NY_Borough


            def display_neighborhood_map(highlight_nhood, hlight_grp):
                neighbourhoods_collection = mongo_connect()  # Assuming you have a working mongo_connect function
                neighbourhoods_mongo = neighbourhoods_collection.find({})

                features = [{
                    'neighbourhood': feature['properties']['neighbourhood'],
                    'neighbourhood_group': feature['properties']['neighbourhood_group'],
                    'geometry': shape(feature['geometry']),
                    'highlight': (feature['properties']['neighbourhood'] == highlight_nhood and
                                  feature['properties']['neighbourhood_group'] == hlight_grp)
                } for feature in neighbourhoods_mongo if 'geometry' in feature]

                gdf = gpd.GeoDataFrame(features)

                fig, ax = plt.subplots(1, 1, figsize=(6, 11))
                gdf[gdf['highlight'] == False].plot(ax=ax, color='grey', edgecolor='black')
                gdf[gdf['highlight'] == True].plot(ax=ax, color='red', edgecolor='black', alpha=0.7)

                ax.set_title(
                    f'Neighborhoods in {highlight_nhood} Area of {hlight_grp} (Highlighted in red)')
                st.pyplot(fig)


            # Example usage:
            display_neighborhood_map(highlight_neighbourhood, highlight_group)

        else:
            # Display message if no results found
            st.write("No listings found for this search criteria.")

if selected == "Hawaii":
    st.title("Data for Hawaii")
    HI_hood = st.selectbox("Neighborhood", HI_Boroughs)
    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)

    # Get listings for the hood selected
    filtered_HI_hood = filter_neighborhood_group(HW_staging, HI_hood)

    upper_range_HI = int(max(tup[10] for tup in filtered_HI_hood))

    # Add a slider for minimum and maximum price
    min_price_HI, max_price_HI = st.slider("Price Range ($)", 1, upper_range_HI, (1, upper_range_HI))

    # Filter data based on price range
    filtered_HI_price = filter_price(filtered_HI_hood, min_price_HI, max_price_HI)

    if st.button("Search"):
        if len(filtered_HI_price) > 0:
            # Display the count of results for the slider
            filtered_count_HI = len(pd.DataFrame(filtered_HI_price))
            st.success(f"{filtered_count_HI} listings were fetched for {HI_hood}.")

            # Extract longitude (index 4) and latitude (index 5)
            latitude_HI = [item[4] for item in filtered_HI_price]
            longitude_HI = [item[5] for item in filtered_HI_price]
            neighborhood_HI = [item[14] for item in filtered_HI_price]

            # Create a DataFrame with lat and lon columns
            filtered_map_data_HI = pd.DataFrame(
                {'lat': latitude_HI, 'lon': longitude_HI, 'neighborhood_area': neighborhood_HI})

            # Create a scatter map using Plotly Express
            fig_HI = px.scatter_mapbox(
                filtered_map_data_HI,
                lat="lat",  # Replace with your actual column name for latitude
                lon="lon",  # Replace with your actual column name for longitude
                hover_name="neighborhood_area",  # Customize hover information
                zoom=10,  # Adjust the initial zoom level
                color_discrete_sequence=["red"],
                opacity=0.9,  # Adjust marker opacity
                size_max=15,  # Adjust marker size
                width=950,
                height=700,
                # Custom marker settings
                custom_data=['lat', 'lon', 'neighborhood_area']
            )

            # Set the map style (you can choose other styles as well)
            fig_HI.update_layout(mapbox_style="carto-positron")

            # Display the map
            st.plotly_chart(fig_HI)

        else:
            # Display message if no results found
            st.write("No listings found for this search criteria.")

if selected == "New Jersey":
    # Display the 'Coming Soon banner'
    st.subheader('Coming Soon ...', divider='rainbow')
    st.caption('Hold on tight now. We are working to make it :rainbow[fabulous] for you '
               ':tulip::cherry_blossom::rose::hibiscus::sunflower:')
    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)

if selected == "Georgia":
    # Display the 'Coming Soon banner'
    st.subheader('Coming Soon ...', divider='rainbow')
    st.caption('Hold on tight now. We are working to make it :rainbow[fabulous] for you '
               ':tulip::cherry_blossom::rose::hibiscus::sunflower:')

    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)

if selected == "Dev Stack/Team":
    st.subheader('Development Stack', divider='rainbow')
    st.write(":gray[The development stack we used for this project includes:]")
    st.write('''
    - :gray[Python]
    - :gray[MongoDB]
    - :gray[PostgresSQL]
    - :gray[Streamlit]
    - :gray[Amazon S3]
                 ''')
    st.subheader('We present the :rainbow[Group 5] Team!', divider='rainbow')
    # Using columns for side-by-side display
    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)


def build_feedback_form():
    """
  This function builds the feedback form using Streamlit elements.
  """
    with st.form("feedback_form"):
        rating = st.number_input("Rate your experience (1-5)", min_value=1, max_value=5)
        subject = st.text_input("Subject")
        feedback = st.text_area("Your Message")
        submitted = st.form_submit_button("Submit")
        return rating, subject, feedback, submitted


if selected == "Contact Us":
    st.header('Contact Us', divider='rainbow')

    # Call the function to display the form
    rating, subject, feedback, submitted = build_feedback_form()

    if submitted:
        st.success(f"Thank you for your feedback! Rating: {rating}, Subject: {subject}, Feedback: {feedback}")
    else:
        st.write("")
    st.sidebar.caption("APAN 5400 Project Solution by Group 5")
    st.sidebar.image("images/logo.svg", width=220)
