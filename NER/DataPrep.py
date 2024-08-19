from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome (optional)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (optional)

# Initialize the WebDriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Open the website
    driver.get("https://bootstrapshuffle.com/classes")

    # Wait for the page to load and class elements to be present
    wait = WebDriverWait(driver, 10)

    # Wait for card elements to be present
    card_elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card"))
    )

    for card_element in card_elements:
        try:
            # Extract card header
            card_header = card_element.find_element(By.CSS_SELECTOR, "h5.card-header").text

            # Extract list group items
            list_group_elements = card_element.find_elements(By.CSS_SELECTOR, "div.list-group.list-group-flush a")
            list_group_items = [item.text for item in list_group_elements]

            print(f"Card Header: {card_header}")
            print("List Group Items:")
            for item in list_group_items:
                print(f"- {item}")

        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Error processing card: {e}")

        # Wait a bit before processing the next card
        time.sleep(1)

finally:
    # Close the WebDriver
    driver.quit()
