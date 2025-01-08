# Step 1: Use an official Python runtime as the base image
FROM python:3.10-slim

# Step 2: Set environment variables to avoid Python writing .pyc files
# and to ensure it outputs logs directly to the terminal
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the current directory contents into the container
COPY . /app/

# Step 5: Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 6: Expose port 8000 (default for Django)
EXPOSE 8000

# Step 7: Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
