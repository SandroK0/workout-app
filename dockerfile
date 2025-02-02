# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "run.py"]
