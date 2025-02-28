from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

class NoContentException(Exception):
    def __init__(self, message="No content found"):
        self.message = message
        super().__init__(self.message)


class Scrapper:
    def __init__(self):
        self._driver = None

    def set_driver(self, browser: str, url: str) -> None:
        if not browser or not url:
            raise ValueError("Browser and URL must be provided.")
        
        if browser.lower() == 'chrome':
            self._driver = webdriver.Chrome()  
        elif browser.lower() == 'firefox':
            self._driver = webdriver.Firefox()  
        elif browser.lower() == 'safari':
            self._driver = webdriver.Safari()  
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        self._driver.get(url)


    def check_original_price(self, timeout: float) -> tuple[str, str]:
        try:
            wait = WebDriverWait(self._driver, timeout)

            try:
                after_sale_price = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay"))
                ).text.strip()
                
            except:
                after_sale_price = "No Sale"
            
            try:
                original_price = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-small.aok-align-center > span > span.aok-relative > span.a-size-small.a-color-secondary.aok-align-center.basisPrice > span > span:nth-child(2)")
                    )
                ).text.strip()
            except Exception:
                original_price = after_sale_price
            
            print(original_price)
            print(after_sale_price)

            return original_price, after_sale_price


        except TimeoutException as e:
            print(f"Error during fetching the price: {e}")
            return "", ""

        finally:
            if self._driver:
                self._driver.quit()

    def send_email(self, original_price: str, after_sale_price: str) -> None:
        SMTP_SERVER = config.SMTP_SERVER
        SMTP_PORT = config.SMTP_PORT
        SENDER_EMAIL = config.SENDER_EMAIL
        SENDER_PASSWORD = config.SENDER_PASSWORD
        RECEIVER_EMAIL = config.RECEIVER_EMAIL

        if original_price == after_sale_price:
            body = f"This product has no sale! Original price is {original_price}"
        elif original_price == "" or after_sale_price == "":
            raise NoContentException("Body is empty") 
        else:
            original_price = f"Original price is: {original_price}"
            after_sale_price = f"Sale price is: {after_sale_price}"
            body = original_price + "\n" + after_sale_price

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "Amazon Sales are comming!"
        msg.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
                print("Email sent successfully!")

        except smtplib.SMTPException as e:
            print(f"Error senging email: {e}")
