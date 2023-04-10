# Base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the producer file to the container
ADD . /app

RUN pip install kafka-python
RUN pip install load_dotenv

# Run the socket server
CMD ["python", "producer.py"]


