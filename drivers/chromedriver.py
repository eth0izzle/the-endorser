from selenium import webdriver


def get(config_drivers):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1024x3000')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X)"
                                "AppleWebKit/602.1.50 (KHTML, like Gecko)"
                                "Version/10.0 Mobile/14A403 Safari/602.1")

    return webdriver.Chrome(executable_path=config_drivers.chrome, chrome_options=chrome_options)
