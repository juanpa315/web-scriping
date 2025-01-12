from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import json

from selenium.webdriver.common.keys import Keys

# User questions

type_property = input("Tipo Propiedad:\n - 1 Casa\n - 2 Apartamento\nEnter your choice (1 or 2): ")

page_number = input("Número de Página: ")

output_file_name = input("Nombre del archivo de salida: ")

print("\nCollected Answers:")
print(f"Tipo Propiedad: {type_property}")
print(f"Número de Página: {page_number}")
print(f"Nombre del archivo de salida: {output_file_name}")


#set up
driver = webdriver.Chrome()
driver.get("https://www.realityrealtypr.com/")
driver.maximize_window()

# Locators
option_propiedades = "//*[@id='navbar']//a[text()='PROPIEDADES']"
btn_ver_resultados = "//button[contains(@class, 'submitBtn') and text()='Ver Resultados']"
targets = "//*[contains(@class, 'col-xs-12 col-sm-4 result')]//h3[@class='list-main-title']//a"

def find_element_by_xpath(element):
    try:
        element = driver.find_element(By.XPATH, element)
        return element
    except NoSuchElementException:
        print(f"Element not found with XPath: {element}")
        return None

# Perform item search
search_criteria = ''
if type_property == "1" :
    search_criteria = "Residential:1"
elif type_property == "2":
    search_criteria = "Residential:5"
else:
    print("invalid property")

element = find_element_by_xpath(option_propiedades)
element.click()

dropdown_element = driver.find_element(By.XPATH, "//select[@name='search[property_type]' and contains(@class, 'searchField')]")
dropdown = Select(dropdown_element)
dropdown.select_by_value(search_criteria)

element = find_element_by_xpath(btn_ver_resultados)
element.click()


# Get web data from realityrealtypr.com 
results = driver.find_elements(By.XPATH,  targets)
data = []

for result in results:
    title = result.get_attribute("title")
    url = result.get_attribute("href")
    data.append({"url": url, "title": title})

#Print data into json format
json_data = json.dumps(data, indent=2, ensure_ascii=False)
print(json_data)
driver.quit()