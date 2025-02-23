from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
import sys
from selenium.common.exceptions import NoSuchElementException
import json

from selenium.webdriver.common.keys import Keys

# Criterios de entrada

propiedad = input("Tipo Propiedad:\n - 1 Casa\n - 2 Apartamento\nEnter your choice (1 or 2): ")

numero_pagina = input("Número de Página: ")

nombre_archivo_salida = input("Nombre del archivo de salida (sin extension): ")
nombre_archivo_salida+=".json"

'''
print("\nCollected Answers:")
print(f"Tipo Propiedad: {propiedad}")
print(f"Número de Página: {numero_pagina}")
print(f"Nombre del archivo de salida: {nombre_archivo_salida}")
'''

#set up
driver = webdriver.Chrome()
driver.get("https://www.realityrealtypr.com/")
driver.maximize_window()

def open_new_tap(url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    

# Localizadores
opcion_propiedades = "//*[@id='navbar']//a[text()='PROPIEDADES']"
btn_ver_resultados = "//button[contains(@class, 'submitBtn') and text()='Ver Resultados']"
resultados_busqueda = "//*[contains(@class, 'col-xs-12 col-sm-4 result')]//h3[@class='list-main-title']//a"
resultados_busqueda2 = "//*[@class='result-content']"
pagina= f"//*[contains(@class, 'btn-default')][{numero_pagina}]"

def find_element_by_xpath(element):
    try:
        element = driver.find_element(By.XPATH, element)
        return element
    except NoSuchElementException:
        print(f"Element not found with XPath: {element}")
        return None

# Perform item search
tipo_propiedad = ''
if propiedad == "1" :
    tipo_propiedad = "Residential:1"
elif propiedad == "2":
    tipo_propiedad = "Residential:5"
else:
    print("invalid property")

element = find_element_by_xpath(opcion_propiedades)
element.click()

dropdown_element = driver.find_element(By.XPATH, "//select[@name='search[property_type]' and contains(@class, 'searchField')]")
dropdown = Select(dropdown_element)
dropdown.select_by_value(tipo_propiedad)

element = find_element_by_xpath(btn_ver_resultados)
element.click()

# ir a la pagina seleccionada
try:
    pagina_seleccionada = driver.find_element(By.XPATH, pagina)
    pagina_seleccionada.click()
    print("loctor: ", pagina_seleccionada)
except NoSuchElementException:
    print("Página no existe, por favor intente nuevamente")
    sys.exit()


# Obtener datos dentro de realityrealtypr.com 
propiedades_encontradas = driver.find_elements(By.XPATH,  resultados_busqueda2)
data = []

for propiedad in propiedades_encontradas:
    
    url = propiedad.find_element(By.XPATH, ".//h3/a").get_attribute("href")
    print("url", url)
    original_winow = driver.current_window_handle
    open_new_tap(url)
    
    
    titulo = driver.find_element(By.XPATH, "//*[@class='col-xs-12 col-sm-8']//h1").text
    ciudad = driver.find_element(By.XPATH, "//*[@class='col-xs-12 col-sm-8']//p").text
    precio = driver.find_element(By.XPATH, "//*[@class='sale-rent-title']").text
    descripcion = driver. find_element(By.ID, "home").text 
    flyer = driver.find_element(By.XPATH, "//div[@class='col-xs-12 col-sm-4 title-side']//a[@target='_blank']").get_attribute("href")

    imagenes = driver.find_elements(By.XPATH, "//*[@class='thumb']//img")
    url_imagenes = []
    contador = 1  

    for imagen in imagenes:
        ruta_imagen = imagen.get_attribute("src")  
        url_imagenes.append(ruta_imagen) 
        print(f"Imagen {contador}: {ruta_imagen}")  
        contador += 1  


    driver.close()
    driver.switch_to.window(original_winow)

    data.append({"url": url, "title": titulo, "city":ciudad, "price": precio, "description": descripcion, "images": url_imagenes, "Flyer": flyer})
    
    

#Print data into json format
json_data = json.dumps(data, indent=2, ensure_ascii=False)
print(json_data)

with open(nombre_archivo_salida, "w", encoding="utf-8") as file:
    file.write(json_data)  # Write the JSON string to the file

print("JSON data successfully saved to output.json")
driver.quit()