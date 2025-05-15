import time

import dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from logs.logs import Logs
from utils.deleteFiles import deleteFiles
from utils.captchaHandler import yesCaptchaHandler



class LoginEcac():

    @staticmethod
    def alterProfile(driver, CLIENT_CNPJ):
        try:
            formattedCNPJ = '{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}'.format(*CLIENT_CNPJ)

            Logs.log_step(f"-----------CNPJ IDENTIFICADO: {formattedCNPJ}-----------")

            driver.cdp.click_if_visible('//*[@id="btnPerfil"]')

            Logs.log_step("-----------Alteração de perfil iniciada-----------")

            driver.cdp.send_keys('//*[@id="txtNIPapel2"]', CLIENT_CNPJ)
            Logs.log_step("-----------CNPJ inserido em input-----------")

            driver.cdp.gui_click_element('#formPJ > input.submit')
            driver.reconnect()
            Logs.log_sucess("-----------CNPJ Submetido-----------")

            sleep(2.4)
        except Exception as e:
            Logs.log_fail(f'Erro ao trocar usuario {e}')
            raise(Exception)

    @staticmethod
    def loginECAC(driver):
        try:
            driver.cdp.click_if_visible('/html/body/div[2]/div/div[2]/div/form/div[2]/p[2]/input')
            Logs.log_step("-----------BOTÃO DE LOGIN COM CERTIFICADO CLICADO-----------")
        except Exception as e:
            Logs.log_fail("-----------ERRO AO CLICAR NO BOTÃO DE LOGIN COM CERTIFICADO-----------")
            raise Exception(f"Erro ao clicar no botão de login: {e}")

        sleep(5)
        driver.cdp.click_if_visible('//*[@id="login-certificate"]')
        Logs.log_step("-----------CLICANDO BOTÃO CERTIFICADO-----------")
        sleep(3)

        yesCaptchaHandler(driver)
        sleep(2.1)

        max_tries = 0
        success = False

        while max_tries < 5 and not success:
            try:
                driver.cdp.find_element('//*[@id="menu-servicos"]')
                Logs.log_sucess("-----------LOGIN REALIZADO COM CERTIFICADO-----------")
                success = True

            except Exception as e:
                
                max_tries += 1
                time,sleep(300)
                Logs.log_fail(f"Tentativa {max_tries} - Erro ao verificar login com certificado: {e}")
                driver.activate_cdp_mode('https://cav.receita.fazenda.gov.br/autenticacao/login')
                sleep(3)  # tempo para recarregar

                try:
                    driver.cdp.click_if_visible('/html/body/div[2]/div/div[2]/div/form/div[2]/p[2]/input')
                    sleep(5)
                    driver.cdp.click_if_visible('//*[@id="login-certificate"]')
                    sleep(3)
                    yesCaptchaHandler(driver)
                    sleep(2.1)
                except Exception as inner_e:
                    Logs.log_fail(f"Erro ao tentar refazer login: {inner_e}")

        if not success:
            raise Exception("Falha ao realizar login após 5 tentativas.")
    