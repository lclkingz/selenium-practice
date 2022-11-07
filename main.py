from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import time
import random


class AutomateList:
    USERNAME = "jason-automation"
    PASSWORD = "passwordqwerty!@#"

    def __init__(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options, service_log_path='./chromeDriver')
        self.wait = WebDriverWait(self.driver, 10)

    def sign_in(self):
        print("Sign in")
        login_page = None
        self.driver.get("https://todo-list-login.firebaseapp.com/#!/")
        main_page = self.driver.current_window_handle
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-social btn-github']"))).click()
        time.sleep(3)
        # change handles to access login page
        for handle in self.driver.window_handles:
            if handle != main_page:
                login_page = handle

        # authorize user if required
        try:
            if login_page is not None:
                print("Switch to login window")
                self.driver.switch_to.window(login_page)
                # login page, fill in username, password and sign in
                self.driver.find_element(By.ID, "login_field").send_keys(self.USERNAME)
                self.driver.find_element(By.ID, "password").send_keys(self.PASSWORD)
                self.driver.find_element(By.XPATH, "//input[@name='commit']").click()
                print("Fill in username, password and sign in")
                time.sleep(3)

                for handle in self.driver.window_handles:
                    if handle == login_page:
                        self.wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[ @ id = 'js-oauth-authorize-btn']"))).click()
        except NoSuchElementException:
            pass
        except NoSuchWindowException:
            pass

        # let page load, back to main page
        print("Switch to main window")
        self.driver.switch_to.window(main_page)

    def sign_out(self):
        print("Sign out")
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-default']").click()

    def fill_in_to_do_list(self):
        print("Filling in to do list")
        for i in range(1, 11):
            string = self.get_random_string()
            self.driver.find_element(By.XPATH, "//input[@ng-model='home.list']").send_keys(string)
            self.driver.find_element(
                By.XPATH, "//button[@class='btn btn-success btn-block glyphicon glyphicon-plus task-btn']").click()

    def get_random_string(self):
        length = random.randint(5, 10)
        letters = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rdm_string = ''.join(random.choice(letters) for x in range(length))
        print(f"Generated random string: {rdm_string}")
        return rdm_string

    def delete_from_list(self):
        count = 0
        for element in self.driver.find_elements(By.CLASS_NAME, 'disney1'):
            count += 1
            if count < 5:
                continue
            else:
                print("Deleting list no. " + str(count))
                element.find_element(By.CLASS_NAME, 'row').find_element(By.CLASS_NAME, 'col-xs-1').\
                    find_element(By.CLASS_NAME, 'btn').click()


if __name__ == '__main__':
    automate = AutomateList()
    automate.sign_in()
    time.sleep(3)
    automate.fill_in_to_do_list()
    time.sleep(1)
    automate.sign_out()
    time.sleep(3)

    automate.sign_in()
    time.sleep(3)
    automate.delete_from_list()
    time.sleep(3)
    automate.sign_out()
    time.sleep(3)
    automate.driver.quit()
