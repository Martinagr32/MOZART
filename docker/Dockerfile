# Base image
FROM python:3
# Copy the requirements txt file with all our dependencies
COPY requirements.txt ./ 
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt  
# Copy the app in the image

COPY docker.py ./  
# Define a default command to execute
CMD [ "python", "./docker.py" ]