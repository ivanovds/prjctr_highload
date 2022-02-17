FROM python:slim-buster
WORKDIR /app
COPY ["app/requirements.txt","./"]
EXPOSE 8000
RUN pip3 install -r requirements.txt