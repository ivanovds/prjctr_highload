FROM python:3.8-slim-buster
WORKDIR /app
COPY ["web-app/requirements.txt","./"]
EXPOSE 8000
RUN pip3 install -r requirements.txt