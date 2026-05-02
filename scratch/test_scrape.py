from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId=68341"
driver.get(url)

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tData tbody tr")))
    rows = driver.find_elements(By.CSS_SELECTOR, ".tData tbody tr")
    print(f"Found {len(rows)} rows")
    for i, row in enumerate(rows):
        cols = row.find_elements(By.TAG_NAME, "td")
        print(f"Row {i}: {len(cols)} columns")
        if len(cols) > 0:
            print(f"  First cell: {cols[0].text}")
except Exception as e:
    print(f"Error: {e}")

driver.quit()
