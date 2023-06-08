# Base image 
FROM python:3.8-slim-buster

# Copy the current directory contents into the container

COPY . /travel

#Set the working directory in the container to travel

WORKDIR /travel

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install the required dependencies 

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Define the command to run the app when the container starts

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Docker file created in the reference of
# https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker