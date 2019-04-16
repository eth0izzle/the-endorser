import os
from drivers import IPHONE_UA
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get(driver_path):
    if not os.path.exists(driver_path):
        raise FileNotFoundError("Could not find phantomjs executable at %s. Download it for your platform at http://phantomjs.org/download.html", driver_path)

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = IPHONE_UA

    driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=driver_path)
    driver.set_window_size(1024, 3000)

    return driver
