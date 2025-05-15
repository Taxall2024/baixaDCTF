import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Driver.driver_funcs import initiateWebDriver,getting_to_DCTF_page,baixando_DCTF
from loginEcac.loginEAlterAccount import LoginEcac as login
from seleniumbase import SB
from utils.deleteFiles import deleteFiles
from Driver.driver_funcs import exitsECACSafely

def isAuthPage(driver):
        return ('/autenticacao' in driver.get_current_url() or
                'sso.acesso.gov.br' in driver.get_current_url())




class EcacBaixaAndUploadPerdComps():

    @staticmethod
    def get_and_upload_perdcomps(cnpj,company_name):

        _cnpj = cnpj
        _company_name = company_name

        download_dir = os.path.abspath("downloads")
        os.makedirs(download_dir, exist_ok=True)

        with SB(uc=True, headed=True, headless2=False, incognito=True, external_pdf=True, maximize=True) as sb:

            driver = initiateWebDriver(sb)
            
            if isAuthPage(driver):

                    #login.loginECAC(driver)
                    time.sleep(30)
                    try:
                        login.alterProfile(driver,_cnpj)
                    
                        getting_to_DCTF_page(driver)
                                      
                        baixando_DCTF(driver)

                        exitsECACSafely(driver)
                        
                        #deleteFiles(downloads_folder)

                    except:
                        driver.activate_cdp_mode('https://cav.receita.fazenda.gov.br/ecac/')
                        pass

if __name__=='__main__':

        
    EcacBaixaAndUploadPerdComps.get_and_upload_perdcomps('17704522000177','HORUS CENTRO MEDICO')
                
