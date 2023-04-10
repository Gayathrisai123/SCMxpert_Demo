FROM python:3.11

# Set the working directory to /app
WORKDIR /final/app

# copy requirements.txt file from the current directory of the host machine inside the Docker image
COPY ./requirements.txt /final/app/requirements.txt

# Install required packages
RUN pip install --no-cache-dir --upgrade -r /final/app/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /final/app

# Expose port 80 for the API
EXPOSE 8080

 # Set the entrypoint

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]