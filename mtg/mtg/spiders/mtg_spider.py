import scrapy
import yaml

image_base_url = "http://magiccards.info/scans/"
card_base_url = "http://magiccards.info"

resources = yaml.load(open("..\\resources.yaml", "r"))



class QuotesSpider(scrapy.Spider):
    name = "mtg"

    start_urls = yaml.load(open("..\\set_urls.yaml", "r"))

    def parse(self, response):
        log = open("log.log", "w")

        entry = {}

        for row in response.xpath(resources["row_xpath"]):
            try:
                table_data = row.xpath("td/text()")
                entry['number'] = row.xpath("td/text()")[0].extract()
                entry['name'] = row.xpath("td/a/text()")[1].extract()
                entry['type'] = row.xpath("td/text()")[2].extract()
                entry['mana'] = row.xpath("td/text()")[3].extract()
                entry['rarity'] = row.xpath("td/text()")[4].extract()
                entry['artist'] = row.xpath("td/text()")[5].extract()
                entry['edition'] = row.xpath("td[7]/text()").extract()
                entry['card_url'] = card_base_url + \
                                    row.xpath("td[2]/a/@href").extract_first()
                entry['image_url'] = image_base_url + \
                                    row.xpath("td[2]/a/@href").extract_first()
            except IndexError:
                log.write("ERROR:"+ response.url +"\n")
                for datum in row.xpath("//td").extract():
                    log.write("\t" + datum)

        yield entry
