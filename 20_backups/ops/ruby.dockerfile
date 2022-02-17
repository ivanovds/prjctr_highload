FROM ruby:3.1.0

RUN gem install sequel pg pry

WORKDIR /app
