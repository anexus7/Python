import requests
import urllib2
import warnings
import sys
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

def crawler(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for noresult in soup.findAll('div', {'class':'touch'}):
        if noresult.string=='Cant find any file for Given criteria':
            print 'No results found'
            a = raw_input("Press <enter> to continue")
    for link in soup.findAll('a', {'class':"touch"}):
        href = link.get('href')
        title = link.string
        print unicode(title)
        x = raw_input("Do you want to save the file (y/n/e) ? ")
        if(x=='e'):
            exit()
        if(x=='y'):
            print("Downloading " + title + "...")
            get_item(href, title)
        print("\n")
    for link in soup.findAll('a', {'class':"rightarrow"}):
        href = link.get('href')
        crawler(href.replace(" ", "%20"))


def get_item(url, title):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for item_name in soup.findAll('a', {'class':'touch'}):
        if item_name.string=="[ Download File ]":
            down(item_name.get("href"), title)


def down(url, file):
    request = urllib2.Request(url)
    with open (file + '.mp3', 'wb') as f:
        response = requests.get(url, stream = True)
        tlength = response.headers.get('content-length')
        if tlength is None:
            f.write(response.content)
        else:
            dl = 0
            tlength = int(tlength)
            for data in response.iter_content(chunk_size = 4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / tlength)
                sys.stdout.write("\r[%s%s]" % ('#' * done, '-' * (50 - done)))
                sys.stdout.flush()


x = raw_input("Enter the movie name : ")
y = raw_input("Enter the format : ")
url = "http://pagalworld.co/search/" + x.replace(" ", "%20") + "/" + y + "/1.html"
crawler(url)
