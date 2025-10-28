# ---------- Build stage ----------
FROM public.ecr.aws/docker/library/python:3.11-alpine3.22 AS builder

# Set working directory
WORKDIR /app

# Copy requirements.txt and install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt -t .

# Copy app source
COPY . .

# Set the Lambda handler
CMD ["main.lambda_handler"]
