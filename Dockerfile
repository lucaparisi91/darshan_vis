# Use Ubuntu as the base image
FROM ubuntu:latest

# Set maintainer information
LABEL maintainer="l.parisi@epcc.ed.ac.uk"

# Update package index and install basic tools (optional)
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a simple hello world script
RUN echo '#!/bin/bash' > hello.sh && \
    echo 'echo "Hello, World!"' >> hello.sh && \
    echo 'echo "Welcome to your Docker container!"' >> hello.sh && \
    chmod +x hello.sh

# Set the default command to run when container starts
CMD ["./hello.sh"]