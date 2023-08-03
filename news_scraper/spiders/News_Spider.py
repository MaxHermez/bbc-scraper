import scrapy
from news_scraper.items import Article
from datetime import datetime


class NewsSpider(scrapy.Spider):
    name = "bbc_news"
    allowed_domains = ["www.bbc.com"]
    start_urls = [
        "https://www.bbc.com/news/newsbeat",
    ]

    def parse(self, response: scrapy.http.Response):
        # Base case: if we're not on the news page, stop
        if "https://www.bbc.com/news/" not in response.url:
            return
        # if the page has an <article> tag, then it's an article page
        if response.css("article"):
            yield from self.parse_article(response)
        # otherwise, collect the links to the articles on the page
        else:
            # collect all hrefs
            article_links = response.css("a::attr(href)").getall()
            # add the domain to the links that don't have it
            article_links = [
                "https://www.bbc.com" + link if link.startswith("/") else link
                for link in article_links
            ]
            # filter out links that aren't in the /news section
            article_links = [
                link
                for link in article_links
                if link.startswith("https://www.bbc.com/news/")
            ]
            # follow each link
            for link in article_links:
                yield response.follow(link, callback=self.parse)

    def parse_article(self, response: scrapy.http.Response):
        # Extract the information from the article page

        title = response.css("#main-heading::text").get()
        date = response.css("time::attr(datetime)").get()
        datetimeObj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        topic = response.css("[class*=TagShareWrapper]::text").get()
        author = response.css("#byline-block:first-child *::text").get()
        related_topics = response.css(
            '[data-component="topic-list"] >> li::text'
        ).getall()
        disallowed_components = [
            "",
            "byline-block",
            "links-block",
            "related-internet-links",
            "topic-list",
        ]
        # all the direct children of the article tag that are divs
        # and have a data-component attribute that isn't in the disallowed_components list
        text = response.xpath(
            "//article/div[@data-component"
            + f' and not(@data-component="{data_component}")'
            for data_component in disallowed_components + "]//text()"
        ).getall()
        related_articles = response.css(
            "[class*=EndOfContentLinksGrid] >> a::attr(href)"
        ).getall()
        url = response.url

        # Create an Article item
        article = Article()
        article["title"] = title
        article["author"] = author
        article["topic"] = topic
        article["related_topics"] = related_topics
        article["date"] = datetimeObj
        article["url"] = url
        article["text"] = text
        article["related_articles"] = [
            "https://www.bbc.com" + link for link in related_articles
        ]
        yield article
