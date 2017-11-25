import os
from drivers import IPHONE_UA
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get(config):
    if not os.path.exists(config.drivers.phantomjs):
        raise FileNotFoundError("Could not find phantomjs executable at %s. Download it for your platform at http://phantomjs.org/download.html", config.drivers.phantomjs)

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = IPHONE_UA

    driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=config.drivers.phantomjs)
    driver.set_window_size(1024, 3000)

    return driver
