'''from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import unittest

from Locators.locators import Locators
from Pages.loginPage import LoginPage
from Pages.homePage import HomePage
import HtmlTestRunner


class LoginTet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_login_not_valid(self):
        driver = self.driver
        login = LoginPage(driver)
        login.enter_username('Admin')
        login.enter_password('wrongPassword')
        login.click_login()
        actual_text = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.XPATH, Locators.alert_message_xpath))
        ).text
        self.assertIn('Invalid credentials', actual_text)

    def test_login_valid(self):
        login = LoginPage(self.driver)
        login.enter_username('Admin')
        login.enter_password('admin123')
        login.click_login()

        expected_url = 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))

        self.assertEqual(self.driver.current_url, expected_url)

        homePage = HomePage(self.driver)
        homePage.click_dropdown()
        homePage.logout()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Test Completed")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output='C:/Users/Utente/Desktop/MAX/automation testing/Selenium/loginProject/Reports'))'''

'''from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import HtmlTestRunner



# Define Locators
class Locators:
    username_field_xpath = "//input[@name='username']"
    password_field_xpath = "//input[@name='password']"
    login_button_xpath = "//button[@type='submit']"
    alert_message_xpath = "//div[@class='oxd-alert-content oxd-alert-content--error']"
    dropdown_xpath = "//span[@class='oxd-userdropdown-tab']"
    logout_xpath = "//a[text()='Logout']"


# Define HomePage Class
class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def click_dropdown(self):
        self.driver.find_element(By.XPATH, Locators.dropdown_xpath).click()

    def logout(self):
        self.driver.find_element(By.XPATH, Locators.logout_xpath).click()

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

        self.username_textbox_xpath = Locators.username_field_xpath
        self.password_textbox_xpath = Locators.password_field_xpath
        self.login_button_xpath = Locators.login_button_xpath

    def enter_username(self, username):
        self.driver.find_element(By.XPATH, self.username_textbox_xpath).clear()
        self.driver.find_element(By.XPATH, self.username_textbox_xpath).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(By.XPATH, self.password_textbox_xpath).clear()
        self.driver.find_element(By.XPATH, self.password_textbox_xpath).send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, self.login_button_xpath).click()


# Define Test Class
class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize the browser and open the application URL."""
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_login_not_valid(self):
        """Test login with invalid credentials."""
        login = LoginPage(self.driver)
        login.enter_username('Admin')
        login.enter_password('wrongPassword')
        login.click_login()

        # Wait for the error message and verify its text
        actual_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Locators.alert_message_xpath))
        ).text
        self.assertIn('Invalid credentials', actual_text, "Error message not found or incorrect.")

    def test_login_valid(self):
        """Test login with valid credentials."""
        login = LoginPage(self.driver)
        login.enter_username('Admin')
        login.enter_password('admin123')
        login.click_login()

        # Verify the URL after successful login
        expected_url = 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
        self.assertEqual(self.driver.current_url, expected_url, "Login was not successful.")

        # Logout
        homePage = HomePage(self.driver)
        homePage.click_dropdown()
        homePage.logout()

    @classmethod
    def tearDownClass(cls):
        """Close the browser after all tests are completed."""
        cls.driver.close()
        cls.driver.quit()
        print("Test Completed")


# Run the tests and generate an HTML report
if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output='./Reports'))  # Change the output directory as needed'''

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import HtmlTestRunner
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Define attributes to extract
ATTRIBUTE_NAMES = ['id', 'name', 'class', 'xpath']

def extract_element_data(element):
    """Extract relevant data from a web element."""
    tag_name = element.tag_name
    text = element.text.strip()
    
    for attr in ATTRIBUTE_NAMES:
        value = element.get_attribute(attr)
        if value:
            return [tag_name, attr, value, text, attr.upper()]
    
    return None  # Skip elements without useful attributes

# Initialize WebDriver and extract data
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
driver.implicitly_wait(10)

all_elements = driver.find_elements(By.XPATH, "//*")
data = [extract_element_data(element) for element in all_elements if extract_element_data(element)]

driver.quit()

# Save data to CSV
csv_filename = "training_data.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["tag_name", "attribute_name", "attribute_value", "text", "locator_type"])
    writer.writerows(data)

print(f"Data extracted and saved to {csv_filename}")

# Load and train ML model
data = pd.read_csv(csv_filename)
X = pd.get_dummies(data[['tag_name', 'attribute_name', 'attribute_value', 'text']])
y = data['locator_type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Model trained with accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Define Locators
class Locators:
    username_field = {"primary": (By.XPATH, "//input[@name='username']"), "alternate": (By.NAME, "username")}
    password_field = {"primary": (By.XPATH, "//input[@name='password']"), "alternate": (By.NAME, "password")}
    login_button = {"primary": (By.XPATH, "//button[@type='submit']"), "alternate": (By.CSS_SELECTOR, "button.orangehrm-login-button")}
    alert_message = {"primary": (By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']"), "alternate": (By.CLASS_NAME, "oxd-alert-content")}
    dropdown = {"primary": (By.XPATH, "//span[@class='oxd-userdropdown-tab']"), "alternate": (By.CLASS_NAME, "oxd-userdropdown-tab")}
    logout_button = {"primary": (By.XPATH, "//a[text()='Logout']"), "alternate": (By.LINK_TEXT, "Logout")}

# Machine Learning Locator Prediction
class LocatorPredictor:
    def __init__(self):
        self.model = model

    def predict_locator(self, element):
        features = {'tag_name': element.tag_name, 'attribute_name': 'name', 'attribute_value': element.get_attribute('name'), 'text': element.text}
        features_df = pd.DataFrame([features])
        features_df = pd.get_dummies(features_df)
        return self.model.predict(features_df)[0]

# Self-Healing Element Finder
class SelfHealingElementFinder:
    def __init__(self, driver, predictor):
        self.driver = driver
        self.predictor = predictor

    def find_element(self, locator_dict):
        for locator_type, locator_value in locator_dict.items():
            try:
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator_value))
                print(f"Element found using {locator_type}: {locator_value}")
                return element
            except:
                print(f"Failed with {locator_type}: {locator_value}, trying next...")
        raise Exception("Element not found with any locator.")

# LoginPage and HomePage
class LoginPage:
    def __init__(self, driver, predictor):
        self.finder = SelfHealingElementFinder(driver, predictor)
    def enter_username(self, username):
        self.finder.find_element(Locators.username_field).send_keys(username)
    def enter_password(self, password):
        self.finder.find_element(Locators.password_field).send_keys(password)
    def click_login(self):
        self.finder.find_element(Locators.login_button).click()

class HomePage:
    def __init__(self, driver, predictor):
        self.finder = SelfHealingElementFinder(driver, predictor)
    def click_dropdown(self):
        self.finder.find_element(Locators.dropdown).click()
    def logout(self):
        self.finder.find_element(Locators.logout_button).click()

# Test Cases
class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.predictor = LocatorPredictor()
    
    def test_login_not_valid(self):
        login = LoginPage(self.driver, self.predictor)
        login.enter_username('Admin')
        login.enter_password('wrongPassword')
        login.click_login()
        actual_text = SelfHealingElementFinder(self.driver, self.predictor).find_element(Locators.alert_message).text
        self.assertIn('Invalid credentials', actual_text)
    
    def test_login_valid(self):
        login = LoginPage(self.driver, self.predictor)
        login.enter_username('Admin')
        login.enter_password('admin123')
        login.click_login()
        WebDriverWait(self.driver, 10).until(EC.url_to_be('https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index'))
        self.assertEqual(self.driver.current_url, 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index')
        homePage = HomePage(self.driver, self.predictor)
        homePage.click_dropdown()
        homePage.logout()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("Test Completed")

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='./Reports'))




