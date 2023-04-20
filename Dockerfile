
FROM python:3.10-slim-buster
WORKDIR /app
RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get -y install git gcc python3-dev
COPY . .
CMD [ "python3","main.py"]
