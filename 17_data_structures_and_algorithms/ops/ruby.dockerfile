FROM ruby:3.1.0

RUN gem install ruby-prof
RUN gem install rspec

WORKDIR /app
