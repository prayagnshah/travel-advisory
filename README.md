# Travel Companion

Live version of the app is available at [Travel Companion](https://travelcompanion.streamlit.app/)

## Description

This [Streamlit](https://streamlit.io/) mini-app generates Travel itinerary for a given city or country according to the type of the travel (solo, trekking, religious, etc.) and number of days. This app tries to use text-davinci-003 model to generate the itinerary. Furthermore, just to avoid the bots users will be able to generate the itinerary for 10 times per day and can be increased by reaching out to me by [Email](prayagshah07@gmail.com).

## Running Locally

1. Clone the repository and install the requirements by typing:
   `pip install -r requirements.txt`
2. Create the account on [OpenAI](https://platform.openai.com/account/api-keys) and get the API key.
3. Create the account on [Upstash](https://console.upstash.com/) to store the user's data and get the API key. This will be used to store the results of the user's query and will not forward the same query to the OpenAI API.
4. Create the account on [Streamlit](https://streamlit.io/) to deploy the app.
   Store the API keys in the `.env` file as follows. Try editing the file `.example.env` to `.env` once the necessary information is stored.

5. Run the app through the terminal by typing:
   `streamlit run app.py`

## Purpose

The purpose of this travel itinerary is to provide a helpful resource for individuals seeking to plan their trip to a specific destination. This itinerary was created with the intention of benefiting the community and ensuring that everyone can take advantage of it.

We believe that travel planning should be accessible and stress-free, and we hope that this itinerary will help individuals plan their trip with ease. We strongly welcome any feedback or suggestions to improve this resource and make it even more helpful for travelers.

You can be reached out to me by [Gmail](prayagshah07@gmail.com) or [LinkedIn](https://www.linkedin.com/in/prayag-shah/).

## Powered by

This example is powered by the following services:

- OpenAI (AI API)
- Upstash (Redis Database)
- Streamlit (App Deployment)
