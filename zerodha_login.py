import os
import time
import pyotp
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from kiteconnect import KiteConnect

api_key = os.getenv("ZERODHA_API_KEY")
api_secret = os.getenv("ZERODHA_API_SECRET")
totp_key = os.getenv("ZERODHA_TOTP_KEY")
user_id = os.getenv("ZERODHA_USER_ID")
user_password = os.getenv("ZERODHA_USER_PASSWORD")

def zerodha_login():
    kite = KiteConnect(api_key=api_key)
    login_url = kite.login_url()
    
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. Go to Zerodha login page
        driver.delete_all_cookies()
        driver.get(login_url)
        time.sleep(3)
        
        # Step 1: Wait & fill userid
        wait.until(EC.presence_of_element_located((By.ID, "userid"))).send_keys(user_id)
        # Step 2: Fill password
        driver.find_element(By.ID, "password").send_keys(user_password)
        # Step 3: Submit login form
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        print("Done with userid and password")
        totp_field = wait.until(EC.visibility_of_element_located((By.ID, "userid")))
        time.sleep(4)

        # Generate and enter TOTP
        totp = pyotp.TOTP(totp_key).now()
        totp_field.clear()
        totp_field.send_keys(totp)
        time.sleep(3)
        
        print("TOTP submitted.")
        print("Waiting for redirect with request_token...")
        time.sleep(4)
        try:
            WebDriverWait(driver, 10).until(lambda d: "request_token=" in d.current_url)
            final_url = driver.current_url
            # Extract request token
            request_token = final_url.split("request_token=")[1].split("&")[0]
            print("Request Token Generated Successfully")
            # Call generate_session
            data = kite.generate_session(request_token, api_secret=api_secret)
            kite.set_access_token(data["access_token"])
            print("Login Successful")
            return kite

        except TimeoutException:
            print("Request token did not appear in URL within expected time.")

    except (TimeoutException, NoSuchElementException) as e:
        print("Something went wrong during login flow:", e)
    except Exception as e:
        print("Unexpected error:", e)

    finally:
        driver.quit()
        
