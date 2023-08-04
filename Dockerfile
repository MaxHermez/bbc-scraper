FROM python:3.11.3

ARG uri
ARG db
ARG col

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV MONGO_URI $uri
ENV MONGO_DB $db
ENV MONGO_COL $col

COPY . .

CMD ["scrapy", "crawl", "bbc_news"]
