#1 importo las libreias que voy a utilizar, 
import time
from datos import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************
# ************************************************************************************************************************



# Creamos la logica para recorrer el dataframe y poder proceder con las eliminaciones 
def recorrer_dtfm(dataframe):
    for index, row in dataframe.iterrows():
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        cedula = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH,"//input[@id='idNumber']")))
        selector = Select(driver.find_element(By.XPATH, "//select[@id='justification']"))
        clave = row['llave']
        cedula.click()
        time.sleep(1)
        cedula.clear()
        cedula.send_keys(clave)
        print(f"Verificando la cedula {clave}.")
        time.sleep(1)
        # Seleccionar la segunda opción del dropdown
        selector.select_by_index(1)
        time.sleep(1)
        button = driver.find_element(By.XPATH,"//button[normalize-space()='Enviar']")
        button.click()
        time.sleep(2)
        #Bajamos hasta el final de la pagina
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Guardamos la tag en la variable obligacion.
            obligacion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@src='./assets/images/obligationlist_icon.png']")))
            # hacemos click en la variable obligacion 
            obligacion.click()
            time.sleep(2)
            # esperamos hasta 15 segundos para que aparezca el tag emergente y lo guardamos en la variable obligabutok
            obligacionbotonemergente = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='accept-alert-modal']")))
            # Procedemos a aceptar o dar click en la  variable obligacionbotonemergente
            obligacionbotonemergente.click()
            time.sleep(2)
            # Guardamos la variable bloqueo con el tag de bloqueo
            spambloqueo = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[@id='eliminar-radio-span']")))
            time.sleep(1)
            # Procedemos a aceptar o dar click en la  variable bloqueo
            spambloqueo.click()
            time.sleep(2)            
            #bajamos hasta el final de la pagina
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Verificamos el boton continuar
            primercontinuar = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='continuar']")))
            time.sleep(2)
            primercontinuar.click()
            time.sleep(5)
            # A continuacion esperamos a que este div emergente aparezaca para poder utilizar el boton continuar en el. 
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='modal-delete']//div[@class='modal-body']")))
            deletebuton = driver.find_element(By.XPATH,"//input[@id='accept-delete']")
            deletebuton.click()
            time.sleep(2)
            #bajamos hasta el final de la pagina
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # trabajamos con la justificacion
            time.sleep(1)
            
            justificacion_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@formcontrolname='justification']")))
            #justificacion_element.click()
            justificacion = Select(justificacion_element)
            justificacion.select_by_value("4")

            time.sleep(2)
            texArea = driver.find_element(By.XPATH,"//textarea[@id='observation']")
            texArea.send_keys("NOVEDAD CON SOLICITUD DE ELIMINACION SAC")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            botonAplicar = driver.find_element(By.XPATH,"//input[@value='Aplicar']")
            botonAplicar.click()
            print(f"{clave},eliminada")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            nuevaConsulta = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='newQuery']")))
            time.sleep(2)
            nuevaConsulta.click()
            time.sleep(5)
            #Al parecer llegamos al final
            #continuamos = input("Llegamos al final Jhojitan: ")      
        except:
                
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'MC.045 ERROR: IDENTIFICACION NO POSEE CUENTAS 1-01')]"))
                    )
                    # Verificar si la cedula existe?
                print(f"{clave},No Extiste")
                continue  # Continuar con el siguiente ID en el ciclo
            except:
                # Si no aparece el mensaje de cédula no existente, verificamos la siguiente opción
                try:
                    # Verificar si la cédula ya está bloqueada o gestionada
                    #Esperamos 5 segundos a que aparezca el estado de la obligacion
                    WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//app-obligations-holder-list[@class='appObligList ng-star-inserted']" ))
                    )
                    try:
                            # Intentamos encontrar el primer span
                           textospam = driver.find_element(By.XPATH, "//span[@class='bloqueados-clr ng-star-inserted']")
                    except NoSuchElementException:
                        
                        try:
                            # Si no se encuentra el primero, intentamos con el segundo
                               textospam = driver.find_element(By.XPATH, "//span[@class='modify-clr ng-star-inserted']")
                        except NoSuchElementException:
                             continue    
                    
                        span_text = textospam.text
                        if span_text in ["B", "R", "V", "F"]:
                          print(f"{clave},{span_text}")    

                except:
                    
                    continue


# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************
# *************************************************************************************************************************



#Instanciamos el driver para iniciar a trabajar con el.
servise = Service("chromedriver.exe") #Usamos el webdriver de google, pues trabajaremos con chrome
driver = webdriver.Chrome(service=servise)
driver.get("https://apps.datacredito.com.co/raw/user-account/login/web/index") #Apuntamos a la URL deseada
driver.maximize_window()
idnumber = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='idNumber']")))
idnumber.send_keys(DATACIDNUMBER) #Capturamos el tag y enviamos la variable como argumento
idpass = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='idPass']")))
idpass.send_keys(DATACIDPASS) #Capturamos el tag y enviamos la variable como argumento

#Como no podemos realizar la autenticacion completamente, procedemos con el autentificador de google
#Esperamos hasta 50 segundos a que la pagina cargue y el elemento 'Entrega de información' esté presente
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

