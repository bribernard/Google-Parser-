import urllib
import mechanize
from bs4 import BeautifulSoup
import re
import csv
import requests

#def get_maven_text(webtxt):

def getMavenLinks(link):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'chrome')]


    term = link.replace(" ", "+")
    #add num=100 after "?=" if you want to search
    query = "https://www.google.com/search?q="+term

    htmltext = br.open(query).read()
    soup = BeautifulSoup(htmltext, "lxml")
    search = soup.findAll('div', attrs= {'id':'search'})
    searchtext = str(search[0])
    soup1 = BeautifulSoup(searchtext, "lxml")
    list_items = soup1.findAll('li')
    regex = "(https://mvnrepository.com/artifact/?\w+.*?%)"
    pattern = re.compile(regex)

    url_results_array = []

    for li in list_items:
        soup2 = BeautifulSoup(str(li), "lxml")
        links = soup2.findAll('a')
        source_link = links[0]
        source_url = re.findall(pattern, str(source_link))
        if len(source_url) > 0:
            url_results_array.append(str(source_url[0].replace("%","")))
    return url_results_array

with open('/Users/brianbernard/Documents/PythonProjects/GoogleParser/peterMissingjars.txt', 'r') as reading:
    with open('/Users/brianbernard/Documents/PythonProjects/GoogleParser/output.csv', 'a') as output:
        w = csv.writer(output, delimiter = ',')
        for c in reading:
            componentSearch = str(c)
            urls = getMavenLinks(componentSearch)
            w.writerow([componentSearch.replace("mvn repository", ""), urls])
            print "Searching for " + componentSearch.replace("mvn repository", "") + ": " + str(urls)
