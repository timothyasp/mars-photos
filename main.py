import re
import urllib2
from BeautifulSoup import BeautifulSoup

baseurl = "http://www.nasa.gov"
basepage = "/mission_pages/mars/images/image-collection_archive_"
pagetype = ".html"

def buildPageUrl(num):
    return baseurl + basepage + str(num) + pagetype

def main():

    soup = BeautifulSoup(urllib2.urlopen(buildPageUrl(1)))

    print soup.title
# TODO: Make this dynamic
    numpages = 46

    images = set();
    for pageNum in range(1, numpages):
        curPage = buildPageUrl(pageNum)
        print "\n\n##############################"
        print "Scanning " + curPage + ": "
        print "##############################\n"
        soup = BeautifulSoup(urllib2.urlopen(curPage))
        for link in soup.find(id='imgGallery5Col').findAll('li'):
            print "     Parsing link ".join(BeautifulSoup(link.p.a.string, convertEntities=BeautifulSoup.HTML_ENTITIES).findAll(text=True))
            linkSoup = BeautifulSoup(urllib2.urlopen(baseurl+link.a['href']))
            downloadBox = linkSoup.find(id='download_image_box')
            if downloadBox != None:
                for imageLink in downloadBox.findAll('a'):
                    img = imageLink['href']
                    if re.search('javascript', img):
                        images.add(re.search(r"""'(?:[^\\']+|\\.)*'""", img).group(0).strip('\''))
                    else:
                        images.add(img)
            else: 
                print "Skipping "
                #linkSoup.find(text="Full Resolution")

    for image in images:
        print baseurl+image

if __name__ == '__main__':
    main()
