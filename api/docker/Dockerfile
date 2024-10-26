FROM python:3.11-slim

# Set environment variables to ensure Python outputs everything to the terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a volume for the application data
VOLUME /app

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
