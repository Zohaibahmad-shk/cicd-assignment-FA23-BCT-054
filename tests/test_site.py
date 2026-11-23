"""
Selenium tests for the CI/CD assignment web page.
Run against the page served from the nginx container.
Target URL comes from the SITE_URL environment variable
(default: http://localhost:8080).
"""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("SITE_URL", "http://localhost:8080")
ROLL_NUMBER = "FA23-BCT-054"
STUDENT_NAME = "Zohaib Ahmad Tariq"


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=options)
    drv.get(BASE_URL)
    yield drv
    drv.quit()


def test_page_title_contains_roll_number(driver):
    """The browser title must contain the roll number."""
    assert ROLL_NUMBER in driver.title


def test_heading_shows_student_name(driver):
    """The main heading must show the student's name."""
    heading = driver.find_element(By.ID, "mainHeading")
    assert heading.text == STUDENT_NAME


def test_roll_number_displayed_on_page(driver):
    """The roll number element must be visible with the correct value."""
    roll = driver.find_element(By.ID, "rollNumber")
    assert roll.is_displayed()
    assert roll.text == ROLL_NUMBER


def test_button_click_shows_message(driver):
    """Clicking the button must display the success message."""
    driver.find_element(By.ID, "msgBtn").click()
    message = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert "button was clicked successfully" in message.text


def test_text_box_input_is_displayed(driver):
    """Text typed in the box must appear on the page after Submit."""
    box = driver.find_element(By.ID, "textInput")
    box.clear()
    box.send_keys("Jenkins CI/CD pipeline test")
    driver.find_element(By.ID, "submitBtn").click()
    shown = driver.find_element(By.ID, "displayText")
    assert "Jenkins CI/CD pipeline test" in shown.text
    # Save one screenshot from a test, as required by the assignment
    driver.save_screenshot(os.path.join(os.path.dirname(__file__), "screenshot_from_test.png"))
