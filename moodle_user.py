from course import Course
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import pickle

class MoodleUser:
    def __init__(self, domain: str, username: str, password: str,
                 driver: WebDriver) -> None:
        self.domain = domain
        self.username = username
        self.password = password
        self.driver = driver
        self.cookies_file = 'cookies.pkl'

        if os.path.exists(self.cookies_file):
            print('loading cookies')
            self.driver.get(self.get_base_url())
            self.load_cookies()
            self.driver.get(self.get_base_url())
            self.automatic_login()
        else:
            print('performing login')
            self.driver.get(self.get_base_url())
            self.login()

    def automatic_login(self) -> None:
        login_url = f'{self.get_base_url()}/login/index.php'
        if self.driver.current_url.startswith(login_url):
            print('performing login')
            self.login()
        else:
            print('skipping login')

    def check_xpath(self, element: WebElement, xpath: str) -> bool:
        return len(element.find_elements(By.XPATH, xpath)) > 0

    def get_base_url(self) -> str:
        return f'https://{self.domain}'

    def get_courses(self) -> list[Course]:
        self.automatic_login()

        courses_url = f'{self.get_base_url()}/my/courses.php'
        self.driver.get(courses_url)

        xpath_courses = '//div[contains(@class, "dashboard-card-deck")]/div'
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_courses))
        )
        element_courses = self.driver.find_elements(By.XPATH, xpath_courses)

        xpath_course_name = '*//span[@class="multiline"]'
        xpath_course_href = 'a'
        xpath_course_category = '*//span[contains(@class, "categoryname")]'
        xpath_course_progress = (
            '*//div[contains(@class, "progress-text")]'
            '/span[2]'
        )

        courses: list[Course] = []
        for element_course in element_courses:
            name = element_course.find_element(
                By.XPATH, xpath_course_name
            ).text

            href = element_course.find_element(
                By.XPATH, xpath_course_href
            ).get_attribute('href')

            category = element_course.find_element(
                By.XPATH, xpath_course_category
            ).text

            progress = int(element_course.find_element(
                By.XPATH, xpath_course_progress
            ).text) if self.check_xpath(
                element_course, xpath_course_progress
            ) else None

            course = Course(name, href, category, progress)
            courses.append(course)
        return courses

    def load_cookies(self) -> None:
        cookies = pickle.load(open(self.cookies_file, 'rb'))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def login(self) -> None:
        id_username = self.driver.find_element(By.ID, 'username')
        id_username.send_keys(self.username)

        id_password = self.driver.find_element(By.ID, 'password')
        id_password.send_keys(self.password)

        id_loginbtn = self.driver.find_element(By.ID, 'loginbtn')
        id_loginbtn.click()

        self.save_cookies()

    def quit(self) -> None:
        self.driver.quit()

    def save_cookies(self) -> None:
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(self.cookies_file, 'wb'))