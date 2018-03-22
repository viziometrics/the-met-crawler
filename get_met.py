import csv
import time 
import urllib2
import requests
from BeautifulSoup import BeautifulSoup

def get_webpage(web_page):
    html_page = urllib2.urlopen(web_page)
    return html_page

def parse_and_get_image(html_page):
    soup = BeautifulSoup(html_page)
    raw_img = soup.find("a", {"name":"#collectionImage"}).find('img')['ng-src']
    img_src = raw_img.split("'")[1]
    return img_src

def save_image_as(img_src, new_img_name):
    r = requests.get(img_src, allow_redirects=True)
    open("images/" + new_img_name + ".jpg", 'wb').write(r.content)

def read_meta_csv(file_name):
    with open(file_name, "rb") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            try:
                html_page = get_webpage(row[40])
                img_src = parse_and_get_image(html_page)
                if img_src:
                    save_image_as(img_src, row)
            except:
                print "Some error occured"
            time.sleep(1.2)
        
def main():
    file_name = "MetObjects.csv"
    read_meta_csv(file_name)

if __name__== "__main__":
    main()