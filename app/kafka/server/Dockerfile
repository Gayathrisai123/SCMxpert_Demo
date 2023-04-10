# Base image
FROM python:3.11


# Set the working directory
WORKDIR /server
# Copy the socket server file to the container
COPY . /server

# Expose the port on which the socket server will run
EXPOSE 5050

# Run the socket server
CMD ["python", "server.py"]



