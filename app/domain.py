import time
import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


cantidad = 4

async def inicializa_navegador():
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')

    # Create a headless Chrome browser instance
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to a website

    # Sign in
    driver.get('https://es.investing.com/portfolio/')
    driver.find_element(by=By.ID, value='loginFormUser_email').send_keys('francofuji@gmail.com')
    driver.find_element(by=By.ID, value='loginForm_password').send_keys('rGWj1XRldr6f')
    driver.find_element(by=By.XPATH, value="//div[@id='loginEmailSigning']//following-sibling::a[@class='newButton orange']").click()
    driver.get('https://es.investing.com/portfolio/')
    return driver

async def obtener_datos(driver):
    tabs = driver.find_element(by=By.CLASS_NAME, value='portfolioTabs').find_elements(by=By.TAG_NAME, value='li')
    portafolio_ids = []
    temporalidades = []
    tablero = {}
    for tab in tabs:
        portafolio_id = tab.get_attribute('data-portfolio-id')
        moneda = tab.get_attribute('title')
        tablero[moneda] = {}
        tablero[moneda]['VF'] = {}
        tablero[moneda]['CF'] = {}

        portafolio_ids.append(portafolio_id)
        tab.click()
        time.sleep(2)
        driver.find_element(by=By.ID, value='technical').find_element(by=By.TAG_NAME, value='a').click()
        time.sleep(2)

        rows = driver.find_element(by=By.CLASS_NAME, value='myPortfolioTbl').find_elements(by=By.CSS_SELECTOR, value='tbody tr')
        for row in rows:
            par = row.find_element(by=By.CSS_SELECTOR, value='a.aqlink').text.split('/')[-1]
            tds = row.find_elements(by=By.CSS_SELECTOR, value=f'td[id^="{portafolio_id}"]:not(.displayNone)')
            for td in tds:
                temporalidad = td.get_attribute('id').split('_')[-1]
                if not temporalidad in temporalidades:
                    temporalidades.append(temporalidad)
                if td.text == 'Venta fuerte':
                    if not temporalidad in tablero[moneda]['VF']:
                        tablero[moneda]['VF'][temporalidad] = []
                    tablero[moneda]['VF'][temporalidad].append(par)
                elif td.text == 'Compra fuerte':
                    if not temporalidad in tablero[moneda]['CF']:
                        tablero[moneda]['CF'][temporalidad] = []
                    tablero[moneda]['CF'][temporalidad].append(par)

    resultado = {temporalidad:{'VF': [], 'CF': []} for temporalidad in temporalidades}
    for moneda in tablero.keys():
        for op in ('VF', 'CF'):
            for temporalidad in tablero[moneda][op].keys():
                if len(tablero[moneda][op][temporalidad]) >= cantidad:
                    resultado[temporalidad][op].append(moneda)
    return resultado
