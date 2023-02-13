FROM python:3.8-alpine

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
COPY . ./

