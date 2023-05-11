FROM bitnami/pytorch

# Switch the user context to root
USER root

# Create missing directory
RUN mkdir -p /var/lib/apt/lists/partial

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    rm -rf /var/lib/apt/lists/*

# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set a build argument for the default port number
ARG PORT=8000

# Set an environment variable for the port number
ENV PORT=$PORT

# Expose the port
EXPOSE $PORT

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT