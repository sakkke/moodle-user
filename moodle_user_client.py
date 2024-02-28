from dotenv import load_dotenv
from moodle_user import MoodleUser
from selenium import webdriver
import os

load_dotenv()

driver = webdriver.Edge()

MOODLE_USER_DOMAIN = os.getenv('MOODLE_USER_DOMAIN')
MOODLE_USER_USERNAME = os.getenv('MOODLE_USER_USERNAME')
MOODLE_USER_PASSWORD = os.getenv('MOODLE_USER_PASSWORD')
moodle_user = MoodleUser(
    MOODLE_USER_DOMAIN,
    MOODLE_USER_USERNAME,
    MOODLE_USER_PASSWORD,
    driver
)