# Use the official Ollama Docker image as the base image
FROM ollama/ollama:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any additional needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME Ollama

# Run Ollama when the container launches
CMD ["ollama", "run"]