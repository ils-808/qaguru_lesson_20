import pytest
from selene import browser
from selenium import webdriver

BASE_URL = 'https://demowebshop.tricentis.com'

@pytest.fixture
def api_url():
    return BASE_URL

@pytest.fixture(scope="function", autouse=True)
def configure_browser():
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--window-size=1920x1080')
    browser.config.driver_options = options
    browser.config.base_url = BASE_URL

    yield

    browser.quit()
