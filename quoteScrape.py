#Quote Scrape - Python3
from lxml import html
import requests
import json
import sys

print("+++ Quote Scrape +++ ")

for arg in sys.argv:
    print(arg)

url = ''
searchName = ''

if len(sys.argv) == 2:
    url = sys.argv[1]
elif len(sys.argv) == 3:
    url = sys.argv[1]
    searchName = sys.argv[2]
else:
    print("Please specify URL in quotes")


page = requests.get(url)
tree = html.fromstring(page.content)


filmName = tree.xpath('//*[@id="main"]/div[1]/div[1]/div/h3/a/text()')[0]

quotesList = tree.xpath('//*[@id="quotes_content"]/div[2]/div/div[@class="sodatext"]/p')


def buildQuoteDict(name, quote):
    quoteDict = {}
    quoteDict['Film']=filmName
    quoteDict['Quote']=quote[1].replace('\n','').replace(':','')

    return quoteDict

quotesDictList = []

for q in quotesList:
    name = q.xpath('a/span/text()')
    quote  = q.xpath('text()')

    if searchName != '':
        if searchName in name:
            quotesDictList.append(buildQuoteDict(filmName, quote))
    else:
        quotesDictList.append(buildQuoteDict(filmName, quote))

json_data = json.dumps(quotesDictList)


quoteFile = open("quotes.json", 'w')
json.dump(quotesDictList, quoteFile)

print(type(json_data))
print(json_data)
print("***")
