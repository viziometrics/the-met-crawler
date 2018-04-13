import re
import csv
import ssl
import time 
import random
import urllib2
import requests
from BeautifulSoup import BeautifulSoup


# original    https://images.metmuseum.org/CRDImages/is/original/sf08-256-270a.jpg
# small image https://images.metmuseum.org/CRDImages/is/web-large/sf08-256-270a.jpg

def get_webpage(web_page):
    html_page = requests.get(web_page)
    return html_page.text

def parse_and_get_image(html_page):
    print html_page
    soup = BeautifulSoup(html_page)
    raw_img = soup.find("a", {"name":"#collectionImage"}).find('img')['ng-src']
    img_src = raw_img.split("'")[1]
    return img_src

def save_image_as(img_src, new_img_name):
    img_src = img_src.replace('web-large', 'original').replace("https://","http://")
    r = requests.get(img_src)
    # try again in smaller quality if cannot find
    if r.status_code != 200:
        img_src = img_src.replace('original', 'web-large')
        r = requests.get(img_src, verify=False)
    open("images/" + new_img_name + ".jpg", 'wb').write(r.content)

def read_meta_csv(file_name):
    images_found = 0
    images_not_found = 0
    with open(file_name, "rb") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            try:
                for col in row:
                    if isValidUrl(col):
                        html_page = get_webpage(col.replace("http://","https://"))
                        img_src = parse_and_get_image(html_page)
                        if img_src:
                            if img_src != '/content/img/placeholders/noimage534x534.png':
                                save_image_as(img_src, row[3])
                                images_found += 1
                            else :
                                images_not_found += 1
                        break

            except Exception as e: 
                print str(e)
                images_not_found += 1
            time.sleep(random.randint(1,9))

    print str(images_found) + " images found"
    print str(images_not_found) + " images not found"

def isValidUrl(input_string):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(input_string)

def main():
    file_name = "MetObjects2.csv"
    read_meta_csv(file_name)

if __name__== "__main__":
    main()
