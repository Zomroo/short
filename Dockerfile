FROM python:3.8-slim-buster
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="Asia/Kolkata"
COPY . .
RUN apt -qq update && apt -qq install -y git
RUN python3 -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt
CMD python3 main.py
