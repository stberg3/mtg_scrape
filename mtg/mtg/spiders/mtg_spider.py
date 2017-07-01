import scrapy
import yaml
import re

image_base_url = "http://magiccards.info/scans/"
card_base_url = "http://magiccards.info"

resources = yaml.load(open("resources.yaml", "r"))

class MtgSpider(scrapy.Spider):
    name = "mtg"

    start_urls = yaml.load(open("set_urls.yaml", "r"))

    def parse(self, response):
        log = open("log.log", "w")

        self.log(response.url)
        entry = {}
        rows = response.xpath(resources["row_xpath"])

        # for row in rows:
        for row in rows:
            i = 0
            try:
                table_data = row.xpath("./td/text()")

                entry['number'] = row.xpath("./td/text()")[0].extract()
                entry['name'] = row.xpath("./td/a/text()").extract_first()
                entry['card_url'] = response.urljoin(
                    row.xpath("./td/a/@href").extract_first())

                try:
                    set_url_part, lang_url_part, card_url_part = \
                        re.search(r'(\w+)/(\w+)/(\w+)\.html',
                            entry['card_url']).groups()
                except AttributeError as ae:
                    self.log("\nBad url? \t{}\n".format(entry['card_url']))

                image_suffix = "{}/{}/{}".format(
                    lang_url_part, set_url_part, card_url_part)

                entry["image_urls"] = ['http://magiccards.info/scans/' + \
                                     image_suffix + ".jpg"]

                entry['type'] = row.xpath("./td/text()")[1].extract()


                # Some entries have no mana cost (lands), so this checks
                # the number of td tags that contain text
                if len(row.xpath("./td/text()").extract()) == 6:
                    entry['mana'] = row.xpath("./td/text()")[2].extract()
                    entry['rarity'] = row.xpath("./td/text()")[3].extract()
                    entry['artist'] = row.xpath("./td/text()")[4].extract()
                    entry['edition'] = row.xpath("./td/text()")[5].extract()[1:]
                else:
                    entry['mana'] = None
                    entry['rarity'] = row.xpath("./td/text()")[2].extract()
                    entry['artist'] = row.xpath("./td/text()")[3].extract()
                    entry['edition'] = row.xpath("./td/text()")[4].extract()[1:]

                entry['card_url'] = card_base_url + \
                                    row.xpath("./td[2]/a/@href").extract_first()

            except IndexError as ie:
                log.write("\n\nERROR:"+ response.url +
                          "\n\tIndexError: {0}".format(ie) + "\n")

                for datum in row.xpath("./td").extract():
                    log.write("\n\t"+ "td[{}]".format(i) + datum)
                    i += 1

            yield entry
            # end for-each loop
        log.close()
