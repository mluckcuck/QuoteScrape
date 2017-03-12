#Quote Scrape - Python3
#12th MArch 2017
from lxml import html
import requests
import json
import sys
import argparse

print("+++ Quote Scrape +++ ")

URLS_JSON = "urls.json"
OUTPUT_PATH = "quotes.json"

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="The URL you wish to check")
parser.add_argument("--searchName", help="Optional, names to return quotes for")
args = parser.parse_args()

urlArg = args.url
searchName = ''
if args.searchName:
     searchName = args.searchName

quotesDictList = []

def buildQuoteDict(filmName, quote):
    quoteDict = {}
    quoteDict['Film']=filmName
    quoteDict['Quote']=quote[1].replace('\n','').replace(':','')

    return quoteDict

def outputToFile(quotesDictList):
    json_data = json.dumps(quotesDictList)
    quoteFile = open(OUTPUT_PATH, 'w')
    json.dump(quotesDictList, quoteFile)
    quoteFile.close()

def getQuotesFrom(url):
    print("Getting Quotes")
    page = requests.get(url)
    tree = html.fromstring(page.content)

    filmName = tree.xpath('//*[@id="main"]/div[1]/div[1]/div/h3/a/text()')[0]
    quotesList = tree.xpath('//*[@id="quotes_content"]/div[2]/div/div[@class="sodatext"]/p')

    for q in quotesList:
        name = q.xpath('a/span/text()')
        quote  = q.xpath('text()')

        if args.searchName:
            if searchName in name:
                quotesDictList.append(buildQuoteDict(filmName, quote))
        else:
            quotesDictList.append(buildQuoteDict(filmName, quote))

if args.url:
    getQuotesFrom(urlArg)
else:
    urls=open(URLS_JSON).read()
    urlList = json.loads(urls)

    for aURL in urlList:
        getQuotesFrom(aURL)


outputToFile(quotesDictList)

print("+++ Done +++")
