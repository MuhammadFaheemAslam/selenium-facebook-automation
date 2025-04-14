from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging, time

def login_facebook(driver, email, password):
    logging.info(f"🔐 Logging in as {email}")
    
    driver.get("https://www.facebook.com/")
    time.sleep(5)

    try:
        # Enter credentials
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass"))).send_keys(password)
        time.sleep(3)
        driver.find_element(By.NAME, "login").click()

        # Wait for page transition or elements
        time.sleep(2)

        # ✅ Check if login was successful by looking for an element only visible on home page
        try:
            # Wait for the search bar on home page (or another unique element)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Facebook']"))
            )
            logging.info(f"✅ Successfully logged in as {email}")
            return True
        except:
            # ❌ If home element not found, check for error message
            try:
                error_div = driver.find_element(By.XPATH, "//div[contains(text(), 'The email or mobile number you entered')]")
                logging.error(f"❌ Login failed: {error_div.text}")
                return False
            except:
                logging.error("❌ Login failed: Incorrect credentials or unknown error.")
            return False

    except Exception as e:
        logging.error(f"❌ Unexpected error logging in: {e}")
        return False
