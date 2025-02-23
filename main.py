from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
import sys
from selenium.common.exceptions import NoSuchElementException
import json

# Criterios de entrada

propiedad = input("Tipo Propiedad:\n - 1 Casa\n - 2 Apartamento\nEnter your choice (1 or 2): ")
tipo_propiedad = ''
if propiedad == "1" :
    tipo_propiedad = "Residential:1"
elif propiedad == "2":
    tipo_propiedad = "Residential:5"
else:
    print("invalid property")
    sys.exit()

numero_pagina = input("Número de Página: ")
nombre_archivo_salida = input("Nombre del archivo de salida (sin extension): ")
nombre_archivo_salida+=".json"

#funciones generales
def open_new_tap(url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    

# Localizadores
locator_opcion_propiedades = "//*[@id='navbar']//a[text()='PROPIEDADES']"
locator_btn_ver_resultados = "//button[contains(@class, 'submitBtn') and text()='Ver Resultados']"
locator_resultados_busqueda = "//*[@class='result-content']//h3/a"
locator_pagina= f"//*[contains(@class, 'btn-default')][{numero_pagina}]"
locator_select_tipo_propiedad = "//select[@name='search[property_type]' and contains(@class, 'searchField')]"
locator_titulo = "//*[@class='col-xs-12 col-sm-8']//h1"
locator_ciudad= "//*[@class='col-xs-12 col-sm-8']//p"
locator_precio= "//*[@class='sale-rent-title']"
locator_descripcion= "home"
locator_imagenes= "//*[@class='thumb']//img"
locator_flyer= "//div[@class='col-xs-12 col-sm-4 title-side']//a[@target='_blank']"

#set up
driver = webdriver.Chrome()
driver.get("https://www.realityrealtypr.com/")
driver.maximize_window()

# 1. Realizar Busqueda
opcion_propiedades = driver.find_element(By.XPATH, locator_opcion_propiedades)
opcion_propiedades.click()

element_tipo_propiedad = driver.find_element(By.XPATH, locator_select_tipo_propiedad)
values_tipo_propiedad = Select(element_tipo_propiedad)
values_tipo_propiedad.select_by_value(tipo_propiedad)

btn_ver_resultados = driver.find_element(By.XPATH, locator_btn_ver_resultados)
btn_ver_resultados.click()

# 2. ir a la pagina seleccionada
try:
    pagina_seleccionada = driver.find_element(By.XPATH, locator_pagina)
    pagina_seleccionada.click()
except NoSuchElementException:
    print("Página no existe, por favor intente nuevamente")
    sys.exit()


# 3. Hacer scrapper
propiedades_encontradas = driver.find_elements(By.XPATH,  locator_resultados_busqueda)
data = []

for propiedad in propiedades_encontradas:
    
    url = propiedad.get_attribute("href")
    original_window = driver.current_window_handle
    open_new_tap(url)
    
    
    titulo = driver.find_element(By.XPATH, locator_titulo).text
    ciudad = driver.find_element(By.XPATH, locator_ciudad).text
    precio = driver.find_element(By.XPATH, locator_precio).text
    descripcion = driver. find_element(By.ID, locator_descripcion).text 
    flyer = driver.find_element(By.XPATH, locator_flyer).get_attribute("href")

    imagenes = driver.find_elements(By.XPATH, locator_imagenes)
    url_imagenes = []

    for imagen in imagenes:
        ruta_imagen = imagen.get_attribute("src")  
        url_imagenes.append(ruta_imagen) 


    driver.close()
    driver.switch_to.window(original_window)

    data.append({"url": url, "title": titulo, "city":ciudad, "price": precio, "description": descripcion, "images": url_imagenes, "Flyer": flyer})
    
    

# 4. generar archivo json con información
json_data = json.dumps(data, indent=2, ensure_ascii=False)
with open(nombre_archivo_salida, "w", encoding="utf-8") as file:
    file.write(json_data)

print("JSON data successfully saved to output.json")
driver.quit()