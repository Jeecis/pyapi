FROM python:3.11.5

# Set the working directory in the container
WORKDIR /python

# Copy the current directory contents into the container at /app
COPY . /python

# Install any dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app/app.py"]