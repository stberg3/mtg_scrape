from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

import threading
from PIL import Image
from hashlib import sha1
import urllib, os, sys, html, time

store_directory = "images"
driver = webdriver.Firefox()
query = html.escape(sys.argv[1]).replace(" ", "+").replace(";", "").replace("&#x", "%")

if(len(sys.argv)==2):
    store_directory = sys.argv[1].replace(" ","_")
    driver.get(("https://www.google.com/search?site=&tbm=isch&source=hp&biw=1855&bih=966&q="+query+"&oq="+query+"&gs_l=img.3..0l10.1451.2486.0.2613.8.6.2.0.0.0.67.253.5.5.0....0...1.1.64.img..1.7.253.0.Xy1TKhU0Sz0"))
else:
    driver.get("https://www.google.com/search?site=&tbm=isch&source=hp&biw=1855&bih=966&q=cat&oq=cat&gs_l=img.3..0l10.1451.2486.0.2613.8.6.2.0.0.0.67.253.5.5.0....0...1.1.64.img..1.7.253.0.Xy1TKhU0Sz0")

try:
    os.mkdir(store_directory)
except FileExistsError:
    pass

for i in range(2):
    for i in range(4):
        # Scroll to get the page to generate more images via AJAX
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Pretty inefficient hack to ensure the script waits for more elements
        # to appear on the page
        time.sleep(1)
    try:
        # Click the button taht make more results appear
        driver.find_element_by_id("smb").click()
    except ElementNotInteractableException:
        pass

img_urls = [elem.get_attribute("src") for elem in
                driver.find_elements_by_css_selector("img.rg_ic")]

class DownloadThread(threading.Thread):
    def __init__(self, url, store_directory):
        threading.Thread.__init__(self)
        self.url = url
        self.store_directory = store_directory

    def run(self):
        fname = str(self.store_directory+"/"+(sha1(self.url.encode("utf8")).hexdigest())+
                                               ".jpg")
        tmp_name = urllib.request.urlretrieve(self.url)[0]
        im = Image.open(tmp_name)

        try:
            im.save(fname, "JPEG")
        except OSError:
            pass

threads = []
with open("threading.log", "w") as file:
    file.write("Starting... ")

for url in img_urls:
    if url != None:
        with open("threading.log", "a") as file:
            file.write(("\nDownloading: "+ url[-20:]))

        threads.append(DownloadThread(url, store_directory))

for thread in threads:
    thread.start()

driver.close()
