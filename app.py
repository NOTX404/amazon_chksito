from calendar import month
from os import link
from pickletools import optimize
from pydoc import replace
from ssl import Options
from time import sleep
from selenium import webdriver
import os, json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException


s=Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_experimental_option ('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=s,options=options)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException])

os.system("cls")


class Amazon:
    def __init__(self, data) -> None:
        # esta monda de aca es para invocar en el json, esos dict metidos en data
        self.usuario = data['email']
        self.password = data['password']
        self.name = data['name']
        self.file = data['file']
        self.files = open(self.file).readlines()
        
    def login(self):
        ''' Open website and login in'''        
        
        driver.get("https://www.amazon.es/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
        
        email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email" i]')))
                
        for i in self.usuario:
            email.send_keys(i)
            
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit" i]'))).click()
        
        password = wait.until(EC.presence_of_element_located((By.ID, 'ap_password')))
        
        for i in self.password:
            password.send_keys(i)
        
        wait.until(EC.element_to_be_clickable((By.ID, 'signInSubmit'))).click()
        
        # Verificacion de Login
        try:
            texto_login = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[text()="Cuenta y listas"]')))
            if len(texto_login) > 0 and texto_login[0].is_displayed():
                print("[!]Login completado con exito")
        except:
            driver.delete_all_cookies()
            self.login()
            
    # En el metodo wallet cuando tienes mas de una cc asociada en tu cuenta de amazon se eliminaran automaticamente
    # Esto es para evitar que se paguen con cc's que no son las correspondientes
    
    def wallet(self):
        driver.get("https://www.amazon.es/cpe/yourpayments/wallet?ref_=ya_d_c_pmt_mpo#")
        self.cards_added = driver.find_elements(By.XPATH, '//span[@class="a-size-small pmts-instrument-number-tail"]')
        if len(self.cards_added) > 0:
            for x in range(len(self.cards_added)):
                try:
                    editar = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="modificar método de pago"]')))
                    editar.click()
                    eliminar = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Eliminar de la cartera"]')))
                    eliminar.click()
                    confirm = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="ppw-widgetEvent:DeleteInstrumentEvent"]')))
                    confirm.click()
                except:
                   self.wallet()
        else:
            print("SIN CC")
                  
    def pago(self):
        for line in self.files:
            line = line.split("|")
            self.ccnum = line[0].strip()
            self.month = line[1].strip()
            self.year = line[2].strip()
            self.cvv = line[3].strip()

            driver.get("https://www.amazon.es/gp/prime/pipeline/membersignup?ms3_c=b665df21a856dd4b0176145f5465353b")

            change_id = driver.find_elements(By.XPATH, '//input[@value="cambiar"]')
            if len(change_id) > 0 and change_id[0].is_displayed():
                change = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@value="cambiar"]'))
                )
                change.click()
            add_cc = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="Añadir una tarjeta de crédito o débito"]'))
            )
            add_cc.click()
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@style="display: inline; height: 122px;"]'))
            name_cc = wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@maxlength="50"]'))
            )
            for i in self.name:
                name_cc.send_keys(i)
            cc_num = wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="addCreditCardNumber"]'))
            )
            for i in self.ccnum:
                cc_num.send_keys(i)
            months = Select(wait.until(
                EC.presence_of_element_located((By.XPATH, '//select[@name="ppw-expirationDate_month"]'))
            ))
            months.select_by_visible_text(self.month)
            years = Select(wait.until(
                EC.presence_of_element_located((By.XPATH, '//select[@name="ppw-expirationDate_year"]'))
            ))
            years.select_by_visible_text(self.year)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@style="display: inline; height: 122px;"]'))
            add_event = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//input[@name="ppw-widgetEvent:AddCreditCardEvent"]'))
            )
            add_event.click()
            set_address = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//input[@name="ppw-widgetEvent:SelectAddressEvent"]'))
            )
            set_address.click()
            driver.get("https://www.amazon.es/gp/prime/pipeline/membersignup?ms3_c=b665df21a856dd4b0176145f5465353b")
            pay = wait.until(
                EC.element_to_be_clickable((By.ID, 'wlp-join-prime-button-announce'))
            )
            pay.click()
            try:
                lives = driver.find_elements(By.XPATH, '//*[@class="a-text-left"]')
            except NoSuchElementException:
                pass
            try:
                dead = driver.find_elements(By.XPATH, '//span[text()="Ha ocurrido un error durante la validación de tu método de pago. Por favor, actualízalo o añade un nuevo método de pago e inténtalo nuevamente."]')
            except NoSuchElementException:
                pass
            if len(lives) > 0 and lives[0].is_displayed():
                os.system('cls')
                print("チェッカー|ɢᴀᴛᴇ{ᴀᴍᴀᴢᴏɴ}|ʟɪᴠᴇ: "+self.ccnum+"|"+self.month+"|"+self.year+"|"+self.cvv)
                input("Press enter to continue...")
                os.system('cls')
                self.wallet()
            if len(dead) > 0 and dead[0].is_displayed():
                print("デッド|ɢᴀᴛᴇ{ᴀᴍᴀᴢᴏɴ}|ᴅᴇᴀᴅ: "+self.ccnum+"|"+self.month+"|"+self.year+"|"+self.cvv, end='\r')
                self.wallet()

        
    # aca es donde va a arrancar todos los metodos que hizo, los va a ejecutar en orden
    def run(self):
        self.login()
        sleep(2)
        self.wallet()
        sleep(2)
        self.pago()
        """
         y asi va haciendo poco a poco los metodos, es mejor hacer todo en diferentes metodos para tener control detallado de cada parte, si un proceso es un muy largo, partirlo en dos
        """

# pondremos lo que va a iniciar el programa, lo comentamos por ahora para no tener errores de sintaxis
if __name__ == '__main__':
	with open('./config.json') as config_file:
		data = json.load(config_file)

    
bot = Amazon(data)
bot.run()
# en esta parte debe declarar la variable bot con la clase y sacando los datos email y pass, luego bot.run para correr el metodo run, que es donde tiene todas las funciones que puso ahi, es donde va correr todo en resumen
