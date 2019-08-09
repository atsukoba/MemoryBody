import requests
import cv2
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = requests.get(url)
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


user_id = input("put your instagram user name:")

url = f"https://www.instagram.com/{user_id}/"

options = Options()
options.set_headless(True)
driver = webdriver.Chrome(chrome_options=options,
                          executable_path='./chromedriver')
driver.get(url)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "lxml")

res = requests.get(url)

pathes = [img["src"] for img in soup.find_all("img")]

img_size = 200

tile = np.zeros([200*4, 200*6, 3])  # 4 x 6

for i in range((4*6)-2):  # 22
    row_idx = i // 6
    col_idx = i % 6
    img = cv2.resize(url_to_image(pathes[i]), (200, 200))
    print("Now downloading picture {}...".format(i))
    tile[200*row_idx:200*(row_idx+1),
         200*col_idx:200*(col_idx+1), :] = img

tile = tile.transpose(1, 0, 2)

cv2.imwrite("sample_texture.png", tile)
print("Saved your img file for Texture")
