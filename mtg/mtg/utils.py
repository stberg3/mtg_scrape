import scrapy

image_base_url = "http://magiccards.info/scans/"
card_base_url = "http://magiccards.info"

def parse_row(row):
    entry = {}
    entry['number'] = row.xpath("td/text()")[0].extract()
    entry['name'] = row.xpath("td/text()")[1].extract()
    entry['type'] = row.xpath("td/text()")[2].extract()
    entry['mana'] = row.xpath("td/text()")[3].extract()
    entry['rarity'] = row.xpath("td/text()")[4].extract()
    entry['artist'] = row.xpath("td/text()")[5].extract()
    entry['edition'] = row.xpath("td/text()")[6].extract()
    entry['card_url'] = card_base_url + \
                        row.xpath("td[2]/a/@href").extract_first()
    entry['image_url'] = image_base_url + \
                        row.xpath("td[2]/a/@href").extract_first()
