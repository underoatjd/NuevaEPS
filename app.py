#1 importo las libreias que voy a utilizar, 

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Variables de autenticacion y lectura de cedulas
Usuario = os.environ.get("usuarioNEPS")
Clave = os.environ.get("claveNEPS")
dataframe = pd.read_csv("cedulas.csv")



#Listas para capturar informacion
capturaInformacion = pd.DataFrame(columns=[
    "Tipo de identificacion",
    "Numero de identificacion",
    "Tipo de afiliado",
    "Regimen",
    "Sexo",
    "Edad",
    "Nombre",
    "Categoria",
    "Telefono fijo",
    "Telefono móvil"
])


# Creamos la logica para recorrer el dataframe y poder proceder con las eliminaciones 
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def capturarCedulas(dataframe):
    for index, row in dataframe.iterrows():
        time.sleep(1)
        cedulaDataframe = str(row['cedula'])
        
        # Ingreso de cédula en el formulario
        tipoAfiliacion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@formcontrolname='tipoDocumento']")))
        tipoAfiliacion = Select(tipoAfiliacion)
        tipoAfiliacion.select_by_value("3")
        
        identificacionCedula = driver.find_element(By.XPATH,"//input[@type='text ']")
        identificacionCedula.clear()
        identificacionCedula.send_keys(cedulaDataframe)
        botonConsulta = driver.find_element(By.XPATH,"//button[normalize-space()='ACEPTAR']")
        botonConsulta.click()

        # Intentamos capturar la información de la tabla
        try:
            # Aumentamos el tiempo de espera a 20 segundos para dar más margen
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@id='respuesta']")))

            # Aquí va el código para extraer los datos de la tabla
            tipo_id = driver.find_element(By.XPATH, "//tr[2]/td[1]").text.strip().replace("Tipo de identificación", "").strip()
            numero_id = driver.find_element(By.XPATH, "//tr[2]/td[2]").text.strip().replace("Número de identificación", "").strip()
            tipo_afiliado = driver.find_element(By.XPATH, "//tr[5]/td[1]").text.strip().replace("Tipo de afiliado", "").strip()
            regimen = driver.find_element(By.XPATH, "//tr[5]/td[2]").text.strip().replace("Régimen", "").strip()
            sexo = driver.find_element(By.XPATH, "//tr[5]/td[3]").text.strip().replace("Sexo", "").strip()
            edad = driver.find_element(By.XPATH, "//tr[5]/td[4]").text.strip().replace("Edad", "").strip()
            nombre = driver.find_element(By.XPATH, "//tr[6]/td[1]").text.strip().replace("Nombre", "").strip()
            categoria = driver.find_element(By.XPATH, "//tr[9]/td[2]").text.strip().replace("Categoría", "").strip()
            telefono_fijo = driver.find_element(By.XPATH, "//tr[9]/td[3]").text.strip().replace("Teléfono fijo", "").strip()
            telefono_movil = driver.find_element(By.XPATH, "//tr[9]/td[4]").text.strip().replace("Teléfono móvil", "").strip()

            # Agregar los datos al DataFrame
            capturaInformacion.loc[len(capturaInformacion)] = [
                tipo_id, numero_id, tipo_afiliado, regimen, sexo, edad, nombre, categoria, telefono_fijo, telefono_movil
            ]

            print(f"Información capturada para cédula {cedulaDataframe}:")
            print(capturaInformacion.tail(1))  # Muestra los últimos datos capturados
        
        except TimeoutException as e:
            print(f"Tiempo de espera agotado para la cédula {cedulaDataframe}. Intentando manejar el error de advertencia...")

            # Intentamos capturar el error del botón de advertencia
            try:
                # Esperamos que el botón 'OK' esté presente
                botonAdvertencia = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"//button[normalize-space()='OK']")))
                botonAdvertencia.click()
                print(f"Se hizo clic en el botón OK para la cédula {cedulaDataframe}")
            except TimeoutException:
                print(f"No se pudo encontrar el botón 'OK' para la cédula {cedulaDataframe}, revisa el flujo.")

        except NoSuchElementException as e:
            print(f"Error al capturar los datos para la cédula {cedulaDataframe}: {e}")
        
        # Pausa antes de continuar con la siguiente cédula
        time.sleep(1)

    # Al finalizar, puedes guardar el DataFrame con los datos recopilados en un archivo CSV
    capturaInformacion.to_excel("informacion_afiliados.xlsx", index=False)
    print("Proceso completado. Los datos se han guardado en 'informacion_afiliados.xlsx'.")




#Instanciamos el driver para iniciar a trabajar con el.
servise = Service("chromedriver.exe") #Usamos el webdriver de google, pues trabajaremos con chrome
driver = webdriver.Chrome(service=servise)
driver.get("https://solucionjb.nuevaeps.com.co/consultas-portal-w/#/") #Apuntamos a la URL deseada
driver.maximize_window()


botonUserExterno = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[normalize-space()='USUARIO EXTERNO']")))
print(botonUserExterno)
botonUserExterno.click()

# Realizamos la autenticacion con las variables de entorno definidas al principio
try:
    
    identificacion = driver.find_element(By.XPATH,"//input[@type='text']")
    identificacion.send_keys(Usuario)
    contraseña = driver.find_element(By.XPATH,"//input[@type='password']")
    contraseña.send_keys(Clave)
    selectorTI = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@formcontrolname='tipoDocumento']")))
    selectorTI = Select(selectorTI)
    selectorTI.select_by_value("4")
    botonIngresar = driver.find_element(By.XPATH,"//button[@type='submit' and contains(@class, 'btn-principal')]")
    botonIngresar.click()
    botonConcultaAfiliado =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='CONSULTA AFILIADO']")))
    botonConcultaAfiliado.click()

except:
    input("Error de Autenticacion")
    



capturarCedulas(dataframe)
    
