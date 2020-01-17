#########################################################
#  File: stock.py
#  Author: Christopher Beeman
#  Scrapes Market Watch for a companies ticker
#  then gets the companies stock data from yahoo finance 
#########################################################

import requests
from bs4 import BeautifulSoup
from csv import writer

'''
Gets a company's ticker to be used in the yahoo finance search url
Param: company being researched
Returns the ticker
'''
def get_abbrev(company):

    web_search = "https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup="+ company +"&Country=all&Type=All"
    response = requests.get(web_search)
    soup = BeautifulSoup(response.text, 'html.parser')

    res = soup.find('td')

    logo = res.find('a')

    return logo.text

'''
Gets the data associated with the stock being searched for
Param: company's ticker
Return a dictionary with different stock data
'''
def get_data(abbrev):

    # Gets the url being parsed and creates a Beautiful Soup object to parse the webpage
    url = "https://finance.yahoo.com/quote/" + abbrev + "?p=" + abbrev + "&.tsrc=fin-srch"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # The div containing price and change in price
    info = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find_all('span')

    price = info[0].text
    change = info[1].text

    # This section contains the stock information
    headers = soup.find_all(class_="C($primaryColor) W(51%)")
    summary = soup.find_all(class_="Ta(end) Fw(600) Lh(14px)")

    head = []
    # list of all the stock data
    dat = []
    # contains the header-data strings
    sentences = []

    for i in range(0, len(summary)):
        # creates a string of the header and data associated with that header
        head.append(headers[i].find('span').text)
        s = headers[i].find('span').text + ": "

        span = summary[i].find('span')
        if (span):
            dat.append(summary[i].text)
            s += span.text
        else:
            dat.append(summary[i].text)
            s += summary[i].text

        sentences.append(s)

    data = {
        'price' : price,
        'change' : change,
        'headers' : head,
        'summary' : dat,
        'sentences' : sentences,
    }

    return data


company = input("Search for company ('q' to quit): ").lower()
while company != 'q':
    abbrev = get_abbrev(company)
    data = get_data(abbrev)
    print()
    for s in data['sentences']:
        print(s)
    # print(data['sentences'])
    print()
    company = input("Search for company ('q' to quit): ").lower()