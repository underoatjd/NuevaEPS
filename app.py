#1 importo las libreias que voy a utilizar, 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


Usuario = 900986188
Clave = "Seguros2022"

#Instanciamos el driver para iniciar a trabajar con el.
servise = Service("chromedriver.exe") #Usamos el webdriver de google, pues trabajaremos con chrome
driver = webdriver.Chrome(service=servise)
driver.get("https://solucionjb.nuevaeps.com.co/consultas-portal-w/?usuario=770867ff3754fe2499e183a39e90f36a#/%23") #Apuntamos a la URL deseada
driver.maximize_window()
tagUsuario = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='idNumber']")))
tagUsuario.send_keys(Usuario) #Capturamos el tag y enviamos la variable como argumento
tagClave = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='idPass']")))
tagClave.send_keys(Clave) #Capturamos el tag y enviamos la variable como argumento

#Autenticacion
try:
    # Por primera vez utilizamos el manejo de errores en este codigo
    spanEntreInfor = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Entrega de información']"))
    )
#Si el elemento no carga o maneja algun tipo de proceso distinto a la carga del elemento "spanEntreInfor", usara este error.
except:
    print("Elemento no encontrado verifica que no existen ventanas emergentes")

#Hacemos Click, Tab y Enter en el elemento en el que estamos trabajando
spanEntreInfor.click()
driver.switch_to.active_element.send_keys(Keys.TAB)
driver.switch_to.active_element.send_keys(Keys.ENTER)

#Le damos 1 segundo al programa para que pued acargar los elementos de la pagina
time.sleep(1)
# Guardar los handles de las pestañas abiertas
handles = driver.window_handles
time.sleep(1)
# Cambiar el control a la nueva pestaña (última pestaña)
driver.switch_to.window(handles[-1])

#Cerraremos el boton emergente dandole hasta 50 segundos de espera a que aparezca.
cerrarbton = WebDriverWait(driver, 50).until(
    EC.element_to_be_clickable((By.XPATH, "(//button[@class='close-button'])[1]")))
cerrarbton.click() 

#Damos click en el boton de modificacion para entrar al menu de modificacion.
modificacion = driver.find_element(By.XPATH,"//img[@src='./assets/images/menu_modify_sl.png']")
modificacion.click() 

#Le damos al programa 2 segundos para iniciar la funcion.
time.sleep(2)
#Llamamos la funcion de trabajo que recorrera el dataframe.  

recorrer_dtfm(dataframe)
#recorrer_dtfm(dataframe)

time.sleep(5)


#corremos la funcion y finalizamos el programa

print("Terminamos el programa")

