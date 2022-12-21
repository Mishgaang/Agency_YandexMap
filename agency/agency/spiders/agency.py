import scrapy
from scrapy.utils.response import open_in_browser
from urllib.parse import urlencode

API_KEY = '7d519771f54a35e6362f66c7b4ee8152'


def proxy(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AgencySpider(scrapy.Spider):
    name = 'agency'
    start_urls = [
        'https://yandex.ru/maps/?ll=96.128443%2C4.772478&mode=search&page=2&sctx=ZAAAAAgCEAAaKAoSCavsuyL4a15AEUDDmzV4hU1AEhIJAAAAAID4bUAR2ZlC5zXmVEAiBgABAgMEBSgKOABAkE5IAWIhYWRkX3NuaXBwZXQ9dG9wb255bV9kaXNjb3ZlcnkvMS54YkJyZWFycj1zY2hlbWVfTG9jYWwvR2VvL0xpc3REaXNjb3ZlcnkvRW5hYmxlRGlzY292ZXJ5VGV4dFJlcXVlc3RzPTFiNXJlYXJyPXNjaGVtZV9Mb2NhbC9HZW8vTGlzdERpc2NvdmVyeS9FbmFibGVSZXF1ZXN0cz0xYjpyZWFycj1zY2hlbWVfTG9jYWwvR2VvL0xpc3REaXNjb3ZlcnkvRW5hYmxlRW1wdHlSZXF1ZXN0cz0xYjVyZWFycj1zY2hlbWVfTG9jYWwvR2VvL0xpc3REaXNjb3ZlcnkvRW5hYmxlVmVydGljYWw9MWIwcmVhcnI9c2NoZW1lX0xvY2FsL0dlby9Bc2tEaXNjb3ZlcnlGb3JUb3Bvbnltcz0xYjpyZWFycj1zY2hlbWVfTG9jYWwvR2VvL0xpc3REaXNjb3ZlcnkvRW5hYmxlQ29tbW9uUGljTWVudT0xagJydZ0BzcxMPaABAKgBAL0BnGhu1MIBhwGsy5O%2FBo6Q9KrOBNm27uID%2B6njkwT3vM3hA4Oi0YcE0pGrhYMDxo3jgfsB27y%2Fxb0Gi%2Fyb%2BAW9oP%2FoRfrHpOQD8uDckAS1jdqn5waKo9aeBMb1gNEElLHL3gaB1Pi47wXDpO6vEu6Gju4Dn5H36rME5KSn8gOws4WCgAKe6aWPuga8l5SVtALqAQDyAQD4AQCCAjjQkNCz0LXQvdGC0YHRgtCy0L4g0L3QtdC00LLQuNC20LjQvNC%2B0YHRgtC4INCg0L7RgdGB0LjRj4oCCTE4NDEwNzUwM5ICAzIyNZoCDGRlc2t0b3AtbWFwcw%3D%3D&sll=96.128443%2C4.772478&sspn=246.445312%2C163.550221&text=Агентство%20недвижимости%20Россия&z=2']

    def start_requests(self):
        yield scrapy.Request(url=proxy(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        # open_in_browser(response)
        agency_page_link = response.css('a.search-snippet-view__link-overlay::attr(href)').getall()
        counter_pages = 0
        while counter_pages < len(agency_page_link):
            yield response.follow('https://yandex.ru' + agency_page_link[counter_pages], self.parse_agency)
            counter_pages += 1

    def parse_agency(self, response):
        # open_in_browser(response)

        def extract_with_css(query):
            return response.css(query).getall()

        yield {
            'name': extract_with_css('h1.orgpage-header-view__header::text'),
            'phone': extract_with_css('div.card-phones-view__number span::text'),
            'link': extract_with_css('a.business-urls-view__link::attr(href)')
        }

    # def parse(self, response):
    #     for quote in response.css('li.search-snippet-view'):
    #         yield {
    #             'name': quote.css('div.search-business-snippet-view__title::text').get()
    #         }
