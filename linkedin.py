import logging
import os, re, time, pickle
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException


class LinkedInClient:
    LOGIN_URL = "https://www.linkedin.com/uas/login"
    COOKIE_JAR = os.path.join(os.getcwd(), ".cookies.pkl")

    def __init__(self, email, password, webdriver=None, timeout=3, save_cookie=True):
        if webdriver is None:
            raise ValueError('You must specify a webdriver')

        self.email = email
        self.password = password
        self.webdriver = webdriver
        self.timeout = timeout
        self.save_cookie = save_cookie

    def __enter__(self):
        self.__login()

        return self

    def __exit__(self, type, value, traceback):
        self.webdriver.quit()

    def __login(self, bypass_cookies=False):
        self.webdriver.get(LinkedInClient.LOGIN_URL)

        # let's try to login with a cookie first
        if self.save_cookie and not bypass_cookies:
            try:
                cookies = pickle.load(open(LinkedInClient.COOKIE_JAR, "rb"))
                if cookies:
                    for cookie in cookies:
                        self.webdriver.add_cookie(cookie)

                    logging.info("Attempting to log in with saved cookies from %s ", LinkedInClient.COOKIE_JAR)
                    return
            except FileNotFoundError:
                pass

        self.webdriver.find_element_by_id("session_key-login").send_keys(self.email)
        self.webdriver.find_element_by_name("session_password").send_keys(self.password)
        self.webdriver.find_element_by_name("login").submit()

        try:
            wait = WebDriverWait(self.webdriver, self.timeout)
            wait.until_not(lambda driver: driver.current_url == LinkedInClient.LOGIN_URL)

            user_id = re.search("\"publicIdentifier\":\"(.*?)\"", self.webdriver.page_source)
            if user_id is not None:
                logging.info("Successfully logged in to LinkedIn. Identifier: %s", user_id.group(1))

                # save cookies for next time - delicious
                if self.save_cookie:
                    pickle.dump(self.webdriver.get_cookies(), open(LinkedInClient.COOKIE_JAR, "wb"))
                    logging.info("Saving cookies to %s", LinkedInClient.COOKIE_JAR)
            else:
                logging.warning("Successfully logged in to LinkedIn but failed to extract your identifier.")
        except TimeoutException:
            logging.error("Login failed. Check your username (%s) and password.", self.email)

    def get_endorsements(self, profile_url):
        skills = list()
        self.webdriver.get(profile_url)
        profile_handle = self.webdriver.current_window_handle

        # dismiss the "view with the app" bullshit (we're using iOS UA)
        try:
            self.scroll_to_bottom()
            self.webdriver.find_element_by_css_selector("button.pv-gta-overlay__dismiss").click()
        except (NoSuchElementException, ElementNotVisibleException):
            pass

        user_id = re.search("\"publicIdentifier\":\"(.*?)\"", self.webdriver.page_source)
        if user_id is None:
            logging.warning("Cookie has expired, logging in again...")
            self.__login(bypass_cookies=True)

        name = self.webdriver.find_element_by_class_name("pv-top-card-section__name").text
        dist = "self" if user_id.group(1) in profile_url else self.webdriver.find_element_by_css_selector(".pv-top-card-section__distance-badge .dist-value").text.strip()

        if dist is "":
            logging.warning("%s is not in your network. We may not be able to retrieve any endorsements...", name)

        try:
            self.webdriver.find_element_by_css_selector("button.pv-skills-section__additional-skills").click()
            self.webdriver.execute_script("arguments[0].scrollIntoView();", self.webdriver.find_element_by_css_selector(".pv-featured-skills-section"))
            self.webdriver.execute_script("window.scrollBy(0, -200);") # backin' up, backin' up
        except NoSuchElementException:
            logging.error("%s doesn't have any endorsements or has hidden them!", name)
            return

        skills_elements = self.webdriver.find_elements_by_css_selector("li.pv-skill-entity a.featured-skill-entity-wrapper,a.-skill-entity-wrapper")
        endorsements_counts = list(int(re.sub(r"\D", "", element.find_element_by_class_name("pv-skill-entity__endorsement-count").text)) for element in skills_elements)
        logging.info("Fetching %s endorsements from %s skills for %s (%s).", sum(endorsements_counts), len(skills_elements), name, ("0" if dist == "" else dist) if dist is not None else "self")

        for element in skills_elements:
            skill_name = element.find_element_by_class_name("pv-skill-entity__skill-name ").text

            ActionChains(self.webdriver).key_down(Keys.SHIFT).click(element).key_up(Keys.SHIFT).perform()
            self.webdriver.switch_to_window(self.webdriver.window_handles[-1])

            waiter = WebDriverWait(self.webdriver, self.timeout)
            waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pv-profile-detail__content")))
            self.scroll_to_bottom(self.webdriver.find_element_by_css_selector(".pv-profile-detail__content"))

            endorsers = list()
            for endorser_element in self.webdriver.find_elements_by_css_selector(".pv-endorsement-entity__link"):
                endorsers.append(endorser_element.find_element_by_css_selector(".pv-endorsement-entity__name--has-hover").text)

            self.webdriver.close()
            self.webdriver.switch_to_window(profile_handle)

            skills.append({"name": skill_name, "endorsements": len(endorsers), "endorsers": endorsers})

        return {"name": name, "skills": skills}

    def scroll_to_bottom(self, element=None, timeout=0.5):
        def get_height():
            return self.webdriver.execute_script("return document.body.scrollHeight") if element is None else self.webdriver.execute_script("return arguments[0].scrollHeight", element);

        last_height = get_height()

        while True:
            if element is None:
                self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                self.webdriver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", element)

            time.sleep(timeout)

            new_height = get_height()
            if new_height == last_height:
                break

            last_height = new_height