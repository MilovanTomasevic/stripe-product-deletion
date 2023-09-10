from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def initialize_driver():
    """
    Initialize and configure a Chrome WebDriver instance.
    Returns:
        webdriver.Chrome: A configured WebDriver instance.
    """
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('headless') # will not display the browser window at runtime
    options.add_argument("--window-size=1920x1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    return driver


def login(driver, user_email, user_password):
    """
    Log in to the Stripe dashboard.
    
    Args:
        driver (webdriver.Chrome): WebDriver instance.
        user_email (str): User's email address.
        user_password (str): User's password.
    """
    driver.get("https://dashboard.stripe.com/login")
    wait = WebDriverWait(driver, 5)
    
    # Handle cookie notification
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="​"]/body/div[1]/div/div/div[3]/div[2]/div/div/div/div[2]/div/div[1]/button'))).click()
    
    # Input user email and password
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(user_email)
    password_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="old-password"]')))
    password_field.send_keys(user_password)
    password_field.send_keys(Keys.RETURN)
    print("\n\nSuccessfully logged in...")


def click_archive_products_button(driver):
    """
    Click the 'Archived' button in the Products.

    Args:
        driver (webdriver.Chrome): WebDriver instance.
    """
    archive_products_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dashboardRoot"]/span/div/div/div/div[1]/div[2]/div/div/div[1]/main/div[3]/div/div/div/div[1]/div/div/div[3]/div/div/div/button/div/span')))
    archive_products_button.click()


def click_three_dots_by_aria_controls(driver, aria_controls):
    """
    Click the three-dots button for a specific row identified by 'aria-controls'.

    Args:
        driver (webdriver.Chrome): WebDriver instance.
        aria_controls (str): ARIA controls attribute value.
    """
    try:
        selector = f"button[aria-controls='{aria_controls}']"
        three_dots_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        three_dots_button.click()
    except:
        print("No three-dots button found for this row.")


def is_modal_text_present(driver):
    """
    Check if the modal text is present in the lower part of the modal.

    Args:
        driver (webdriver.Chrome): WebDriver instance.
    """
    try:
        modal_text_bottom = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Are you sure you want to delete this product? This can')]")))
        print("Found text in the lower part of the modal:", modal_text_bottom.text)
    except:
        print("Text not found in the lower part of the modal.")


def click_delete_product_from_table(driver):
    """
    Click the 'Delete product' from products table.

    Args:
        driver (webdriver.Chrome): WebDriver instance.
    """
    try:
        delete_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='delete-product']")))
        delete_option.click()
    except Exception as e:
        print(f"Error clicking 'Delete product' button in the modal: {str(e)}")


def click_delete_product_in_modal(driver):
    """
    Click the 'Delete product' button in the modal.

    Args:
        driver (webdriver.Chrome): WebDriver instance.
    """
    try:
        delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button-element') and contains(., 'Delete product')]")))
        delete_button.click()
    except Exception as e:
        print(f"Error clicking 'Delete product' button in the modal: {str(e)}")


def main(user_email, user_password):
    driver = initialize_driver()
    login(driver, user_email, user_password)
    
    print("Waiting to click on products")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dashboardRoot"]/span/div/div/div/div[1]/div[2]/div/div/div[3]/nav/div/div[5]/div/div[1]/a/div'))).click()
    
    while True:
        try:
            print("Waiting to click on archived products")
            click_archive_products_button(driver)

            # Find all rows in the table
            rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='Table-cell Table-cell--align--right Table-cell--verticalAlign--middle Table-cell--width--minimized Table-cell--wrap--noWrap ListViewItem-cell']")))
            
            if len(rows) > 0:
                row = rows[0]
                aria_controls = row.find_element(By.TAG_NAME, "button").get_attribute("aria-controls")
                click_three_dots_by_aria_controls(driver, aria_controls)

                print("Waiting to click on delete product")
                click_delete_product_from_table(driver)
                
                print("Modal checking...")
                is_modal_text_present(driver)
                print("Waiting to click on the delete product modal")
                click_delete_product_in_modal(driver)
                print("The product has been successfully deleted")

                time.sleep(2)
                # driver.refresh()

            else:
                print("No archived products found.")
                break

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            break
    
    print("\n\nProcess completed. \nIf some products were not deleted, run the script again.\n")
    driver.quit()


if __name__ == "__main__":
    USER_EMAIL = "your_email@example.com"
    USER_PASSWORD = "your_password"

    main(USER_EMAIL, USER_PASSWORD)
