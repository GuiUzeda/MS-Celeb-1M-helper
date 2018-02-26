from bs4 import BeautifulSoup
import urllib2
import os

from threading import Thread
import argparse


import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


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
        p = 500
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            if p == 500:
                logging.debug(status)   
                p=0
            p += 1    

        f.close()

def main(args):



    dest_path = args.dir

    response = urllib2.urlopen(
        'https://msceleb.blob.core.windows.net/ms-celeb-v1-cropped-split?restype=container&comp=list')
    html = response.read()

    soup = BeautifulSoup(html, 'lxml')

    urls=  soup.find_all("url")
    thrs = []
    for thread_number in range (len(urls)):

        a = Th(thread_number, str(urls[thread_number].string), dest_path)
        a.start()
        thrs.append(a)

if __name__ == "__main__":
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(description="A download script for the MS-Celeb-1M's croped DB")
    parser.add_argument("-d", "--dir", help="Directory to save the data",
                        default=os.path.join(cwd, "data"))
    args = parser.parse_args()

    main(args)