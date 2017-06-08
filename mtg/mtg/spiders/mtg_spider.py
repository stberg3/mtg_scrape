import scrapy
import yaml

image_base_url = "http://magiccards.info/scans/"
card_base_url = "http://magiccards.info"

resources = yaml.load(open("resources.yaml", "r"))



class QuotesSpider(scrapy.Spider):
    name = "mtg"

    start_urls = yaml.load(open("set_urls.yaml", "r"))[:10]

    def parse(self, response):
        log = open("log.log", "w")

        entry = {}

        for row in response.xpath(resources["row_xpath"]):
            i = 0
            try:
                table_data = row.xpath("./td/text()")

                entry['number'] = row.xpath("./td/text()")[0].extract()
                entry['name'] = row.xpath("./td/a/text()").extract_first()
                entry['type'] = row.xpath("./td/text()")[1].extract()

                # Some entries have no mana cost (lands), so this checks
                # the number of td tags that contain text
                if len(row.xpath("./td/text()").extract()) == 6:
                    entry['mana'] = row.xpath("./td/text()")[2].extract()
                    entry['rarity'] = row.xpath("./td/text()")[3].extract()
                    entry['artist'] = row.xpath("./td/text()")[4].extract()
                    entry['edition'] = row.xpath("./td/text()")[5].extract()
                else:
                    entry['mana'] = None
                    entry['rarity'] = row.xpath("./td/text()")[2].extract()
                    entry['artist'] = row.xpath("./td/text()")[3].extract()
                    entry['edition'] = row.xpath("./td/text()")[4].extract()

                entry['card_url'] = card_base_url + \
                                    row.xpath("./td[2]/a/@href").extract_first()
                entry['image_url'] = image_base_url + \
                                    row.xpath("./td[2]/a/@href").extract_first()

            except IndexError as ie:
                log.write("\n\nERROR:"+ response.url +
                          "\n\tIndexError: {0}".format(ie) + "\n")

                for datum in row.xpath("./td").extract():
                    log.write("\n\t"+ "td[{}]".format(i) + datum)
                    i += 1

        log.close()

        yield entry
