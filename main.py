from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

#set up
driver.get("https://www.realityrealtypr.com/")
driver.maximize_window()

option_propiedades = "//*[@id='navbar']//a[text()='PROPIEDADES']"
btn_ver_resultados = "//button[contains(@class, 'submitBtn') and text()='Ver Resultados']"
targets = "//*[contains(@class, 'col-xs-12 col-sm-4 result')]"

def find_element_by_xpath(element):
    try:
        element = driver.find_element(By.XPATH, element)
        return element
    except NoSuchElementException:
        print(f"Element not found with XPath: {element}")
        return None

element = find_element_by_xpath(option_propiedades)
element.click()

dropdown_element = driver.find_element(By.XPATH, "//select[@name='search[property_type]' and contains(@class, 'searchField')]")
dropdown = Select(dropdown_element)
dropdown.select_by_value("Residential:1")

element = find_element_by_xpath(btn_ver_resultados)
element.click()


driver.quit()