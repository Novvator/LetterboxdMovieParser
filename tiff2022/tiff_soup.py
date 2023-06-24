import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def desc_scrape_with_selenium(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

    # Set path to the chromedriver executable
    chromedriver_path = "chromedriver.exe"

    # Set up the Selenium WebDriver service
    service = Service(chromedriver_path)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to the URL
    driver.get(url)

    # Wait for the dynamic content to load (you may need to adjust the delay)
    driver.implicitly_wait(3)  # Wait for 5 seconds

    try:
        # Find the element using XPath
        element = driver.find_element(By.XPATH, '//section[contains(@class,"article-content")]')

        # Extract the text from the element
        text = element.text.strip()
    except:
        text = 'No Description'


    return text, driver


url = "https://www.filmfestival.gr/en/program-tiff/global-program"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

films = {}

# Find all film link elements + titles
link_elements = soup.find_all("td", {"class" : "movie-title"})
for link_element in link_elements:
    films[link_element.text.strip()] = link_element.contents[1].attrs['href']
print(len(films)) # 259
with open('tiff2022/movies_scrape.csv', 'w', newline='', encoding='utf-8') as file_out:
    writer = csv.writer(file_out)
    for idx, film in enumerate(films.keys()):
        url_suffix = films[film]
        url_prefix = "https://www.filmfestival.gr" + url_suffix

        description, driver = desc_scrape_with_selenium(url_prefix)
        row = [str(film), url_suffix, str(description)]
        writer.writerow(row)
    driver.quit()

