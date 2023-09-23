import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
URL = "http://localhost:8501/"


from selenium import webdriver


def test_text_input_existence():
    """Test the landing page for streamlit site"""
    driver.get("http://localhost:8501/")
    input_element_locator = (
        By.CSS_SELECTOR,
        "input[aria-label='Enter github repo address']",
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(input_element_locator)
    )
    driver.quit()
    time.sleep(5)


@pytest.mark.skip(reason="Not implemented yet")
def test_get_codebase():
    driver.get("http://localhost:8501/")
    input_element_locator = (
        By.CSS_SELECTOR,
        "input[aria-label='Enter github repo address']",
    )
    text_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(input_element_locator)
    )

    text_input.clear()
    text_input.send_keys("ddomin212/bnb_web")

    submit_button = driver.find_element(
        By.CSS_SELECTOR, "button[kind='secondary']"
    )
    submit_button.click()

    chart_locator = (By.CSS_SELECTOR, "div[class*='stGraphVizChart']")
    chart_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(chart_locator)
    )

    assert text_input.get_attribute("value") == "ddomin212/bnb_web"
    assert "graphviz-chart" in chart_element.get_attribute("id")

    li_locator = (
        By.XPATH,
        "//li[contains(@class,'nav-item')]/a[contains(@class,'nav-link')]/i[contains(@class,'icon bi-file-code')]/ancestor::li",
    )
    li_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(li_locator)
    )
    li_element.click()

    vega_lite_locator = (
        By.CSS_SELECTOR,
        "[data-testid='stArrowVegaLiteChart']",
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(vega_lite_locator)
    )

    selectbox_elements = driver.find_elements(
        By.CSS_SELECTOR, "div.row-widget.stSelectbox"
    )
    assert len(selectbox_elements) == 2

    horizontal_blocks = driver.find_elements(
        By.CSS_SELECTOR, "[data-testid='stHorizontalBlock']"
    )
    assert len(horizontal_blocks) == 2

    for horizontal_block in horizontal_blocks:
        columns = horizontal_block.find_elements(
            By.CSS_SELECTOR, "[data-testid='column']"
        )
        assert len(columns) == 4

    # li_locator = (
    #     By.XPATH,
    #     "//li[contains(@class,'nav-item')]/a[contains(@class,'nav-link')]/i[contains(@class,'icon bi-pen')]/ancestor::li",
    # )
    # li_element = driver.find_element(*li_locator)
    # li_element.click()

    # select_boxes = driver.find_elements(
    #     By.CSS_SELECTOR, "div.row-widget.stSelectbox"
    # )
    # assert len(select_boxes) == 1

    # code_block = driver.find_element(
    #     By.CSS_SELECTOR, "[data-testid='stCodeBlock']"
    # )
    # assert code_block is not None

    # button_locator = (
    #     By.XPATH,
    #     "//div[contains(@class,'row-widget stButton') and @data-testid='stButton']//button/div/p[text()='Show code']",
    # )
    # button = driver.find_element(*button_locator)
    # assert button is not None

    # button.click()

    # code_blocks = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located(
    #         (By.CSS_SELECTOR, "[data-testid='stCodeBlock']")
    #     )
    # )

    # assert len(code_blocks) == 2
