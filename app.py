import streamlit as st
import openai
import os
import redis
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

host = os.environ.get('REDIS_HOST')
port = os.environ.get('REDIS_PORT')
password = os.environ.get('REDIS_PASSWORD')

redis_client = redis.Redis(host=host, port=port, password=password, decode_responses=True)


def get_itinerary(destination_name, type_of_trip, length_of_stay):
    """
    Will store the itinerary in Redis for 7 days and checking the rate limit of the user
    """
    itinerary_key = get_itinerary_key(destination_name, type_of_trip, length_of_stay)
    itinerary = get_itinerary_from_redis(itinerary_key)
    
    if itinerary:
        return itinerary
    
    check_rate_limit()
    
    itinerary = call_openai_api(destination_name, type_of_trip, length_of_stay)
    itinerary = format_itinerary(itinerary)
    
    STORAGE_TIME = 604800
    redis_client.set(itinerary_key, itinerary, ex=STORAGE_TIME)
    
    return itinerary


def get_itinerary_key(destination_name, type_of_trip, length_of_stay):
    """
    Storing the input values to avoid the future API calls
    """
    return f"{destination_name}_{length_of_stay}_{type_of_trip}"


def get_itinerary_from_redis(itinerary_key):
    """
    If the itinerary exists in Redis database, returns it directly without making the API call
    """
    if redis_client.exists(itinerary_key):
        itinerary = redis_client.get(itinerary_key)
        if itinerary:
            return itinerary


def check_rate_limit():
    """
    Checking the count of requests in Redis database and if it exceeds the limit, stops the execution
    """
    global_rate_limit_key = "GLOBAL_RATE_LIMIT"
    global_rate_limit = redis_client.get(global_rate_limit_key)
    
    if global_rate_limit is not None:
        global_rate_limit = int(global_rate_limit)
        request_count = redis_client.incr("Total_Request_Count")
        
        if request_count > global_rate_limit:
            st.write("You have exceeded the maximum number of requests. Please try again tomorrow or reach out to me on [Linkedin](https://www.linkedin.com/in/prayag-shah/) to increase rate-limit.")
            st.stop()
            

def call_openai_api(destination_name, type_of_trip, length_of_stay):
    """
    Making the API call to OpenAI
    """
    # If type of trip is provided, then add it to the prompt
    if type_of_trip:
        prompt = f"Can you recommend a {length_of_stay} day itinerary for {destination_name}? In detail? And they should be in format Day 1, Day 2, etc. Type of trip should be based on {type_of_trip} trip."
    else:
        prompt = f"Can you recommend a {length_of_stay} day itinerary for {destination_name}? In detail? And they should be in format Day 1, Day 2, etc."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=1024,
        n=1,
        stop=None
    )

    return response.choices[0].text.strip()


def format_itinerary(itinerary):
    """
    Showing Day 1, Day 2, etc. in a new line
    """
    return itinerary.replace(":", "\n")
        


# Title
st.title("Travel Advisory")

# Description
description = """Made by [Prayag Shah](https://www.linkedin.com/in/prayag-shah/) with ❤️. Check out the source code at [GitHub](https://github.com/prayagnshah/travel-advisory)."""
st.markdown(description, unsafe_allow_html=True)

# Set the maximum number of words in the destination name
MAX_WORDS= 3

# User's input
destination_name = st.text_input("Enter your destination")

num_words = len(destination_name.strip().split())

# Show a warning message if the number of words exceeds the limit
if num_words > MAX_WORDS:
    st.warning("The destination name should be less than 3 words")
    st.stop()

type_of_trip = st.text_input("Enter the type of trip (e.g. Hiking, Solo, Religious, etc) (optional)")

length_of_stay = st.slider("Enter the length of your stay", 1, 10)

# Read funny loading messages
with open("loading_messages.txt", "r") as f:
    loading_messages = f.readlines()

# Generate itinerary and show loading message
if st.button("Generate Itinerary"):
        
    placeholder = st.empty()
    
    loading_message = random.choice(loading_messages)
    
    # Adding loading message
    with st.spinner(text = loading_message):
        
        # Call the function to generate the itinerary
        itinerary = get_itinerary(destination_name, type_of_trip, length_of_stay)
    placeholder.text("")
    st.success(itinerary)