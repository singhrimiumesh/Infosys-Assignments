from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headfullscreen")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.imdb.com/")
print("Opened IMDb website.")

movie_name = "Singh is King"

search_box = driver.find_element(By.ID, "suggestion-search")
search_box.send_keys(movie_name)
search_button = driver.find_element(By.ID, "suggestion-search-button")
search_button.click()

wait = WebDriverWait(driver, 20)  

wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]")))
first_result = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]")
first_result.click()

wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span")))

title = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span").text
rating = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]").text
year = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a").text

print(f"Title: {title}")
print(f"Year: {year}")
print(f"IMDb Rating: {rating}")

driver.quit()
print("\n\nClosed the browser.")
