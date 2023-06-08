# Base image 
FROM python:3.8-slim-buster

# Copy the current directory contents into the container

COPY . /travel

#Set the working directory in the container to travel

WORKDIR /travel

# Install the required dependencies 

RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the app when the container starts

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]