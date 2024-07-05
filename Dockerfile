# Import base image for python 3
FROM python:3

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY webapp/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY webapp .

# Set the environment variable FLASK_APP to app
ENV FLASK_APP=app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]