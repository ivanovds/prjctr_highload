FROM python:3.9.5-slim-buster

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat 
RUN apt-get install iputils-ping -y

# run entrypoint.sh
ENTRYPOINT ["tail"]
CMD ["-f", "/dev/null"]
