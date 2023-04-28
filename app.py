import requests
import streamlit as st


def get_itinerary(dest_name, length_of_stay):
    # Call the OpenAI API
    response = requests.post(
        "http://localhost:5000/destination",
        json={
            "destination_name": dest_name,
            "length_of_stay": length_of_stay
        }
    )

    # Extract the response text

    itinerary = response.json()["message"]

    format_itinerary = itinerary.replace("Day:", '\n' + "Day")

    return format_itinerary

# Set up the app name


st.title("Travel Advisory")

# Get user input

destination_name = st.text_input("Enter your destination")
length_of_stay = st.slider("Enter the length of your stay", 0, 10)

# Generate itinerary

if st.button("Generate Itinerary"):
    itinerary = get_itinerary(destination_name, length_of_stay)
    st.success(itinerary)
