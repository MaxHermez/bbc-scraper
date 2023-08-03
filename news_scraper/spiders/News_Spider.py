import scrapy
from news_scraper.items import Article

class NewsSpider(scrapy.Spider):
    name = "bbc_news"
    start_urls = [
        'https://www.bbc.com/news',
    ]

    def parse(self, response: scrapy.http.Response):
        # Extract the links to the individual articles on the page
        article_links = response.css('a.gs-c-promo-heading::attr(href)').getall()
        for link in article_links:
            yield scrapy.Request(link, callback=self.parse_article)
    
    def parse_article(self, response: scrapy.http.Response):
        # Extract the title, author, topic, related_topics, cover image, date, and text
        # from the article page
        
        title = response.css('#main-heading::text').get()
        date = response.css('time::attr(datetime)').get() 
        # datetimeObj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        topic = response.css('[class*=TagShareWrapper]::text').get()
        # cover = response.css('[data-component="image-block"] >> img::attr(alt)').get()
        author = response.css('#byline-block:first-child *::text').get()
        related_topics = response.css('[data-component="topic-list"] >> li::text').getall()
        text = response.css('[data-component="image-block"]::text, [data-component="video-block"]::text, [data-component="text-block"]::text').getall()
        url = response.url

        # Create an Article item
        article = Article()
        article['title'] = title
        article['author'] = author
        article['topic'] = topic
        article['related_topics'] = related_topics
        article['date'] = date
        article['url'] = url
        article['text'] = text
        yield article