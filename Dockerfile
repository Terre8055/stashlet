FROM python:3.10-alpine

# Set the working directory
WORKDIR /app


# Copy the requirements.txt file into the container
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application files into the container
COPY . /app

# Expose the port your app runs on
EXPOSE 8080

#Env variables
ENV PYTHONPATH=/app/sus-db/src/

# Command to run your application
CMD ["python", "src/main.py"]

