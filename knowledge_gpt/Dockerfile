# Use Python 3.8 as a base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the command to start the Streamlit app
CMD ["streamlit", "run", "main.py"]
