from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from Test_Locators import locators
import pytest
from Utilities.excel_functions import ExcelFunction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

class Test_Login:

    @pytest.fixture()
    def startup(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.implicitly_wait(10)
        excel_file= locators.Locators.file
        sheet_number=locators.Locators.sheet_no
        self.excel_functions=ExcelFunction(excel_file,sheet_number)
        yield
        self.driver.close()

    def test_login(self,startup):
        self.driver.get(locators.Locators.url)
        self.driver.maximize_window()
        wait=WebDriverWait(self.driver,8)
        start_row = 2
        end_row =9

        for row_no in range(start_row,end_row+1):
            username_value=self.excel_functions.read_data(row_no,5)
            password_value=self.excel_functions.read_data(row_no,6)

            username_element= wait.until(EC.visibility_of_element_located((By.ID,locators.Locators().username_id)))
            username_element.send_keys(username_value)

            password_element= wait.until(EC.visibility_of_element_located((By.ID,locators.Locators().password_id)))
            password_element.send_keys(password_value)

            submit_btn = wait.until(EC.visibility_of_element_located((By.ID, locators.Locators().submit_id)))
            submit_btn.click()

            try:
                wait.until(EC.url_matches((locators.Locators().sucess_url)))
                self.excel_functions.write_data(row_no,7,"TEST PASSED")
                print("successfully logined with {} and {}".format(username_value,password_value))

                logout_btn= wait.until(EC.presence_of_element_located((By.XPATH,locators.Locators().logout)))
                logout_btn.click()

                wait.until(EC.url_matches((locators.Locators().url)))

            except TimeoutException:
                self.excel_functions.write_data(row_no, 7, "TEST FAILED")
                print("Login failed with {} and {}".format(username_value, password_value))

                assert self.driver.current_url== locators.Locators().url
                self.driver.refresh()