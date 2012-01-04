from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from craigslist.items import House

class CraigslistSpider(BaseSpider):
  name = "craigsbot"
  allowed_domains = ["craigslist.org"]
  start_urls = [
      "http://sfbay.craigslist.org/apa/"
  ]

  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    apas = hxs.select('//blockquote//p')
    items = []
    for apa in apas:
      item = House()
      # title
      title = apa.select('a/text()').extract();
      if len(title) > 0:
        item['title'] = title[0].strip()

      # link
      link = apa.select('a/@href').extract()
      item['link'] = link 

      # location
      loc = apa.select('font/text()').extract()
      if len(loc) > 0:
        item['loc'] = loc[0].strip() 
        item['loc'] = str(item['loc'])[1:len(item['loc'])-1]

      # image type
      image = apa.select('span/text()').extract()
      if len(image) > 0:
        item['image'] = image[0].strip() 

      items.append(item)
    return items
