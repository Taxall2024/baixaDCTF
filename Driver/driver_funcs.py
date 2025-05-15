import time
import os

import dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from logs.logs import Logs
from utils.deleteFiles import deleteFiles
from dotenv import load_dotenv

load_dotenv()
folderPath = os.getenv('FOLDER_PATH')
downloadsPath = os.getenv('DOWNLOADS_PATH')



def initiateWebDriver(sb):
    try:
        Logs.log_step("-----------INICIALIZANDO WEBDRIVER-----------")
        sb.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath" : downloadsPath
        })
        sb.activate_cdp_mode(
            'https://cav.receita.fazenda.gov.br/autenticacao/login')

        Logs.log_step("-----------WEBDRIVER INICIALIZADO-----------")

        return sb
    except Exception as e:
        Logs.log_fail('WEBDRIVER NÃO PÔDE SER INICIALIZADO')
        Logs.log_fail(e)


def baixando_DCTF(sb):
    for ano in range(2,6):
        for mes in range(1,13):
            try:
                sb.find_element(f'/html/body/font/center/form/table/tbody/tr[2]/td[2]/h2/select/option[{ano}]').click()
                Logs.log_sucess("Selecionado ano para baixar arquivos ...")
            except Exception as e:
                Logs.log_fail(f"Erro ao selecionar ano {e}")    
            try:
                sb.find_element(f'/html/body/font/center/form/table/tbody/tr[3]/td[2]/select/option[{mes}]').click()
                Logs.log_sucess("Selecionado mês para baixar arquivos ...")
            except Exception as e:
                Logs.log_fail(f"Erro ao selecionar mês {e}")

            try:
                sb.click('/html/body/font/center/form/div[1]/input[1]')
                sleep(2)
                sb.click('//*[@id="divDownload"]/input')
                Logs.log_sucess(f"Arquivo baixado para periodo {mes}/{ano}")
                sleep(3)
            except Exception as e:
                Logs.log_fail(f"Não existe arquivo para o período {mes}/{ano}")
                Logs.log_fail(f"Erro ao baixar elemento {e}")
                pass   



def getting_to_DCTF_page(sb):
    sleep(2)
    sb.cdp.find_element('//*[@id="btn214"]/a').click()
    try:
        sb.reconnect()
        Logs.log_sucess('Clicando Declarações e demonstrativos !')
    except Exception as e:
        Logs.log_fail(f"Erro ao clicar em demonstrativos {e}") 
    
    try:
        sleep(2)
        sb.cdp.find_element('//*[@id="containerServicos214"]/div[1]/ul/li[2]/a').click()
        Logs.log_step("Indo para página de copias de declarações")
    except Exception as e:
        Logs.log_fail(f"Erro ao clicar em Cópia de declaração{e}")
    try:
        sleep(2)
        sb.switch_to_frame('//*[@id="frmApp"]')
        sb.click_link(   
						'DCTF - Declaração de Débitos e Créditos Tributários Federais')
        #sb.click('/html/body/table[1]/tbody/tr[2]/td[2]')
        Logs.log_step("Clicando em DCTF ...")
    except Exception as e:
        Logs.log_fail(f"Erro ao clicar em DCTF{e}")
 
    sleep(20)




def shutdownWebDriver(driver):
    try:
        Logs.log_warning('-----------tentando desligar WEBDRIVER-----------')
        sleep()
        driver.driver.quit()
        Logs.log_warning('-----------DESLIGANDO WEBDRIVER-----------')
    except Exception:
        Logs.log_fail('-----------ERRO AO DESLIGAR WEBDRIVER-----------')
        pass





def exitsECACSafely(sb):
    try:
        Logs.log_warning('-----------tentando sair com segurança-----------')
        sleep(2)
        sb.driver.switch_to.default_content()
        sb.find_element(By.XPATH, '//*[@id="sairSeguranca"]').click()
        Logs.log_warning(
            "-----------SAINDO COM SEGURANÇA, DESATIVANDO WEBDRIVER-----------")
    except Exception as e:
        Logs.log_fail("-----------ERRO AO SAIR COM SEGURANÇA DO ECAC-----------")
        Logs.log_fail(e)


def sendESC(sb):
    sb.driver.send_keys('html', Keys.ESCAPE)


def switchToIFrame(driver):
    try:
        time.sleep(0.25)
        driver.switch_to_frame('//*[@id="frmApp"]')
        Logs.log_step("-----------MUDANÇA DE ACESSO PARA IFRAME FRMAPP-----------")
    except Exception as e:
        Logs.log_fail("-----------ERRO AO ACESSAR IFRAME FRMAPP-----------")
        raise Exception('navigational', 'Erro ao acessar iframe', e)


def returnToMainWindow(sb):
    try:
        deleteFiles(folderPath)
        url = "https://cav.receita.fazenda.gov.br/ecac/"
        sb.open(url)
        Logs.log_step(
            "-----------Retornando para página principal-----------")
    except Exception as e:
        Logs.log_fail("-----------ERRO AO RETORNAR PARA PÁGINA PRINCIPAL-----------")
        raise Exception(
            'navigational', 'Erro ao retornar para página principal', e)


def checkSession(driver):
    wait = WebDriverWait(driver, 5)

    try:
        wait.until(
            EC.visibility_of_element_located((
                By.XPATH, '/html/body/div[1]/div[3]/h1'
            ))
        )
        Logs.log_fail('!!!ALERTA: SESSÃO TERMINADA PELO SISTEMA, REINICIANDO')
    except Exception:
        pass


def findByXpath(driver, locator):
    try:
        checkSession(driver)
        Logs.log_sucess('-----------Clicanco no Xpath -----------')
        return driver.find_element(By.XPATH, locator)
    except Exception as e:
        Logs.log_fail(
            f"-----------ERRO AO ENCONTRAR ELEMENTO: {locator}-----------")
        raise Exception('method', f'Erro ao encontrar por XPATH {locator}', e)


def findById(driver, locator):
    try:
        checkSession(driver)
        return driver.find_element(By.ID, locator)
    except Exception as e:
        Logs.log_fail(
            f"-----------ERRO AO ENCONTRAR ELEMENTO: {locator}-----------")
        raise Exception('method', f'Erro ao encontrar por ID {locator}', e)


def findByClass(driver, locator):
    try:
        checkSession(driver)
        return driver.find_element(By.CLASS_NAME, locator)
    except Exception as e:
        Logs.log_fail(
            f"-----------ERRO AO ENCONTRAR ELEMENTO: {locator}-----------")
        raise Exception('method', f'Erro ao encontrar por CLASS {locator}', e)


def findByCss(driver, locator):
    try:
        checkSession(driver)
        return driver.find_element(By.CSS_SELECTOR, locator)
    except Exception as e:
        Logs.log_fail(
            f"-----------ERRO AO ENCONTRAR ELEMENTO: {locator}-----------")
        raise Exception('method', f'Erro ao encontrar por CSS {locator}', e)


def findByName(driver, locator):
    try:
        checkSession(driver)
        return driver.find_element(By.NAME, locator)
    except Exception as e:
        Logs.log_fail(
            f"-----------ERRO AO ENCONTRAR ELEMENTO: {locator}-----------")
        raise Exception('method', f'Erro ao encontrar por NAME {locator}', e)


def waitForElement(driver, condition):
    try:
        checkSession(driver)
        wait = WebDriverWait(driver, 12)

        return wait.until(condition)
    except Exception as e:
        Logs.log_fail("-----------ERRO AO AGUARDAR ELEMENTO-----------")
        raise Exception('method', 'Erro ao aguardar elemento', e)


def proceedButton(driver):
    try:

        xpaths = [
        '(//a[@aria-label="Next"])[2]',
        '(//a[@aria-label="Next"])[1]']
        def finding_xpath_continue():
            for xpath in xpaths:
                try:
                    # Verificar se o botão de avançar existe para o XPath atual
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    print(f"Botão de avançar encontrado com XPath: {xpath}")
                    return xpath  
                except Exception:
                    continue  
            
        botao_avancar_xpath = finding_xpath_continue()
        botao_avancar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_avancar_xpath))
                )
        
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_avancar)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", botao_avancar)
    
        Logs.log_step('-----------BOTÃO DE PROCEDER CLICADO-----------')

        sleep(2)
    except Exception as e:
        print('Erro ao clicar no botão de proceder')
        raise Exception(
            'navigational', 'Erro ao clicar no botão de proceder', e)

