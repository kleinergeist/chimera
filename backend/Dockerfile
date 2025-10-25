# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt ./

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the image
COPY . .

# Expose port for service
EXPOSE 8000

# Run FastAPI server with Uvicorn
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
