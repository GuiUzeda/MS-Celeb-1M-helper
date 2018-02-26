from bs4 import BeautifulSoup
import urllib2
import os

from threading import Thread

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

dest_path = "data/"

response = urllib2.urlopen(
    'https://msceleb.blob.core.windows.net/ms-celeb-v1-cropped-split?restype=container&comp=list')
html = response.read()

soup = BeautifulSoup(html, 'lxml')

urls=  soup.find_all("url")


class Th(Thread):

    def __init__(self, num, url, path):
        Thread.__init__(self)
        self.num = num
        self.url = url
        #print(self.url)
        self.fname = str(url.split("/")[-1])
        self.path=path

    def run(self):

        f = open(os.path.join(os.getcwd(), self.path, self.fname), 'wb')
        u = urllib2.urlopen(self.url)
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        logging.debug( "Downloading: %s Bytes: %s" % ( self.fname , file_size))
        file_size_dl = 0
        block_sz = 8192
        
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            logging.debug(status) 

        f.close()

thrs = []
for thread_number in range (len(urls)):

    a = Th(thread_number, str(urls[thread_number].string), dest_path)
    a.start()
    thrs.append(a)

