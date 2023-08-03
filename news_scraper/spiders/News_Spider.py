import scrapy
from re import sub
from news_scraper.items import Article
from datetime import datetime

text_junk = [
    r"Follow Newsbeat on[\s\S]*$", # usually appears at the end of each article
    "Image source[\s\S]*?Image caption,? ?\n?", # image captions
]

def clean_text(texts: list[str]) -> str:
    """Joins all the text in a list of strings into a single string, and cleans it up.
    Removes whitespace from the beginning and end of a string, and replaces
    all whitespace in the middle with a single space, except for new lines. Removes any text matching 
    one of the text_junk strings defined above.
    """
    text = ""
    for t in texts:
        text += t
        if not t.endswith(" "): # if the string doesn't end with a space, start a new line
            text += "\n"
    for junk in text_junk:
        text = sub(junk, "", text) # remove junk text
    text = sub(r" {2,}", " ", text) # replace multiple spaces with a single space
    text = text.replace("\n.\n", ".\n") # remove new lines between sentences
    return text


class NewsSpider(scrapy.Spider):
    name = "bbc_news"
    allowed_domains = ["www.bbc.com"]
    start_urls = [
        "https://www.bbc.com/news",
        "https://www.bbc.com/news/newsbeat",
    ]
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES' : {
    #             'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #             'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #         }
    # }

    def parse(self, response: scrapy.http.Response):
        # Base case: if we're not on the news page, stop
        if (
            "https://www.bbc.com/news/" not in response.url
            or "https://www.bbc.com/news/av/" in response.url
            or "https://www.bbc.com/news/world_radio_and_tv/" in response.url
        ):
            return
        # if the page has an <article> tag, then it's an article page
        if response.xpath('//*[@id="main-content"]/article[1]'):
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
        topic = response.xpath(
            '//*[@id="main-content"]/article/header/div[2]/div[2]/div/ul/li/a/text()'
        ).get()
        author = response.xpath(
            '//*[@data-component="byline-block"]/div[1]/div/div/div[1]//text()'
        ).get()
        author_title = response.xpath(
            '//*[@data-component="byline-block"]/div[1]/div/div/div[2]/text()'
        ).get()
        related_topics = response.xpath(
            '//div[@data-component="topic-list"]//li//text()'
        ).getall()
        disallowed_components = [
            "",
            "byline-block",
            "links-block",
            "related-internet-links",
            "topic-list",
        ]
        # all the direct children of the article tag that are divs
        text_xpath = "//article/div[@data-component"
        # and have a data-component attribute that isn't in the disallowed_components list
        for data_component in disallowed_components:
            text_xpath += f' and not(@data-component="{data_component}")'
        text_xpath += "]//text()"
        text = response.xpath(text_xpath).getall()
        # combine text into a single string
        text = clean_text(text)
        related_articles = response.xpath(
            '//*[contains(@class, "EndOfContentLinksGrid")]//a/@href'
        ).getall()
        url = response.url

        # Create an Article item
        article = Article()
        article["title"] = title
        article["author"] = author
        article["author_title"] = author_title
        article["topic"] = topic
        article["related_topics"] = related_topics
        article["date"] = datetimeObj
        article["url"] = url
        article["text"] = text
        article["related_articles"] = [
            "https://www.bbc.com" + link for link in related_articles
        ]
        yield article
