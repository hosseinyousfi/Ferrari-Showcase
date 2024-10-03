# inherit from the base image
FROM python:3.12-slim

# setting work directory
WORKDIR /app

# update pip version
RUN pip install --upgrade pip

# copy requirements
COPY requirements.txt requirements.txt

# env variable
ENV PYTHONBUFFERED=1

# install dependencies
RUN pip install -r requirements.txt

# copy the rest of the application
COPY . .
