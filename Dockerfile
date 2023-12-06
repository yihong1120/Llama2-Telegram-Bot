# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variable to prevent interactive prompts during apt-get commands
ENV DEBIAN_FRONTEND=noninteractive

# Update apt and install required tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    lsb-release \
    apt-transport-https \
    software-properties-common \
    gnupg \
    python3.11 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Add repository and key for Microsoft SQL
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install Microsoft's MSSQL tools and other necessary packages
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools18 && \
    apt-get install -y unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# Add mssql-tools18 to the system PATH
ENV PATH="$PATH:/opt/mssql-tools18/bin"

# Install Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy your application into the container
COPY . /app/
WORKDIR /app/

# Execute app.py and web server of Django when the container starts
CMD ["sh", "-c", "python app.py && cd chatbo_web && python manage.py runserver 8080"]

# To utilise this Dockerfile, first execute the following command in the directory containing the Dockerfile to construct the container image:
# '''bash
# docker build -t chatbot_app .
# '''

# Subsequently, run:
# '''bash
# docker run -p 8080:8080 chatbot_app
# '''
