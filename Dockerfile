# Use the latest version of Ubuntu as the base image
FROM ubuntu:latest

# Set the working directory in the container to /app
WORKDIR /app

# Update the package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential

# Copy the requirements file to the container
COPY requirements.txt /app/
COPY bot.py /app/
COPY .env /app/
# Install the required packages from the requirements file
RUN pip3 install --no-cache-dir -r requirements.txt

# Define the command to run the Flask app
CMD ["python3", "bot.py"]
