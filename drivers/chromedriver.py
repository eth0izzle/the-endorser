import os
from drivers import IPHONE_UA
from selenium import webdriver


def get(driver_path):
    if not os.path.exists(driver_path):
        raise FileNotFoundError("Could not find chromedriver executable at %s. Download it for your platform at https://chromedriver.storage.googleapis.com/index.html?path=2.33/", driver_path)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1024x3000')
    chrome_options.add_argument("user-agent=" + IPHONE_UA)

    return webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
