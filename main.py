import re, sys, os, errno
import urllib2
from BeautifulSoup import BeautifulSoup

download_dir = "/Users/tasp/Dropbox/Personal/Photos/Mars/"

baseurl = "http://www.nasa.gov"
basepage = "/mission_pages/mars/images/image-collection_archive_"
pagetype = ".html"

def buildPageUrl(num):
    return baseurl + basepage + str(num) + pagetype

def cleanTitle(title):
    return re.sub(r'&[^\s]*;', '', title)

def downloadImage(subdir, imgdir, url):
    filename = re.search(r"""[^/]+$""", str(url)).group(0)
    print "Downloading " + filename + "....."

    req = urllib2.Request(baseurl + url)
    req.add_header('Referer', baseurl)

    response = urllib2.urlopen(req)

    directory = download_dir + subdir 
    if not os.path.exists(directory):
        os.makedirs(directory)

    imgdir = directory + '/' + re.sub(' ', '-', imgdir)
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    filepath = imgdir + '/' + filename
    if not os.path.isfile(filepath):
        print "Saving to " + filepath
        output = open(filepath, 'wb')
        output.write(response.read())
        output.close()
    else:
        print "Already downloaded, skipping"

def main():

    soup = BeautifulSoup(urllib2.urlopen(buildPageUrl(1)))

    print soup.title
# TODO: Make this dynamic
    numpages = 46

    for pageNum in range(1, numpages):
        curPage = buildPageUrl(pageNum)
        print "\n\n##############################"
        print "Scanning " + curPage + ": "
        print "##############################\n"
        soup = BeautifulSoup(urllib2.urlopen(curPage))
        for link in soup.find(id='imgGallery5Col').findAll('li'):
            # Get the image title for image subdir
            title = cleanTitle("".join(BeautifulSoup(link.p.a.string).findAll(text=True)))

            linkSoup = BeautifulSoup(urllib2.urlopen(baseurl+link.a['href']))
            downloadBox = linkSoup.find(id='download_image_box')

            # Get modified date for photo organization
            dateText = linkSoup.find(attrs={"name" : "dc.date.modified"})['content']

            if downloadBox != None:
                for imageLink in downloadBox.findAll('a'):
                    img = imageLink['href']
                    if re.search('javascript', img):
                        img = re.search(r"""'(?:[^\\']+|\\.)*'""", img).group(0).strip('\'')

                    # Download the image
                    downloadImage(dateText, title, img)

            else: 
                images = linkSoup.find(text=re.compile(' Full Resolution'))
                if not images == None:
                    img = images.findParent('a')['href']
                    downloadImage(dateText, title, img) 


if __name__ == '__main__':
    main()
