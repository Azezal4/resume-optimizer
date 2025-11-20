# Use an official lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# 1. Copy the requirements file and install the necessary Python packages.
# Using --no-cache-dir reduces the final image size.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the main application script into the container.
COPY app.py .

# 3. Streamlit runs on port 8501 by default. Expose this port.
# Note: This is informative; the port mapping is done in docker-compose.yml.
EXPOSE 8501

# 4. Define the default command to run when the container starts.
# This command starts the Streamlit server, making it accessible externally 
# (0.0.0.0) and running the app.py script.
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]