import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv


# Calling key from environment variables

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initializing the Flask class
app = Flask(__name__)
CORS(app)

# Asking details from the user


@app.route('/destination', methods=["POST"])
def post_destination():

    req_data = request.get_json()
    dest_name = str(req_data.get('destination_name'))
    length_of_stay = str(req_data.get('length_of_stay'))

    # Send an immediate response to the user to indicate that the request is being processed

    response_data = {
        "message": "Building itinerary..."
    }
    response = jsonify(response_data)
    # Use the HTTP status code 202 (Accepted) for a non-final response
    response.status_code = 202

    # Call the OpenAI API

    response = openai.Completion.create(
        engine="text-davinci-002",  # Which GPT-3 engine to use
        prompt="Can you recommend a " + length_of_stay + \
        "day itinerary for " + dest_name + "?" + \
        "in format day1, day2, etc",  # The input text #nopep8
        temperature=0.5,  # How creative the response should be
        max_tokens=500,  # Maximum length of the response
        n=2,  # How many responses to generate
        stop=None  # Text to stop generation at (optional)
    )

    # Extract the response text
    itinerary = response.choices[0].text.strip()

    # As requested JSON input turning the output in JSON format as well
    response_data = {
        "message": itinerary
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
