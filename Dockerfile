# Use the official lightweight Python image.
FROM python:3.12.3-alpine

# Create a working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies listed in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Exposing the port(same in app.py for my on ease)
EXPOSE 8000

# Specify the command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]