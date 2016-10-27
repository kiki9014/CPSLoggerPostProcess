from lxml import html
import requests
import sys

androidMarketUrl = "https://play.google.com/store/apps/details?id="

page = requests.get(androidMarketUrl + "net.skyscanner.android.main")
tree = html.fromstring(page.content)

category = tree.xpath('//span[@itemprop="genre"]/text()')

lat = category[0].encode('ISO-8859-1').decode('UTF-8')
# category[0].encode('UTF-8')

print(lat)