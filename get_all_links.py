from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Konfiguracja filtrowania
USE_FILTER = True  # Zmień na False, jeśli chcesz wszystkie linki bez filtrowania
ALLOWED_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg")  # ignorowane jeśli USE_FILTER = False

# Plik z adresami URL
input_file = "websites_to_get_links_from.txt"

# Wczytaj linki z pliku
with open(input_file, "r") as file:
    urls = [line.strip() for line in file if line.strip()]

# Plik, do którego będą zapisywane linki
output_file = "extracted_links.txt"

# Ustawienia opcji przeglądarki Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Inicjalizacja przeglądarki
print("Inicjalizacja przeglądarki w trybie headless...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    # Otwórz plik do zapisu w trybie append
    with open(output_file, "a", encoding='utf-8') as file:
        for url in urls:
            try:
                print(f"Otwieram stronę: {url}")
                driver.get(url)

                # Oczekiwanie na załadowanie strony
                print("Czekam na załadowanie strony...")
                # Czekamy na załadowanie konkretnego elementu, który zawiera wyniki
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
                )
                
                # Dodatkowe opóźnienie, aby upewnić się, że JavaScript załadował wszystkie elementy
                time.sleep(2)

                print("Strona załadowana, szukam linków...")

                # Znajdź wszystkie elementy <a> w kontenerze wyników wyszukiwania
                link_elements = driver.find_elements(By.CSS_SELECTOR, ".search-results a")

                # Pobierz linki (z filtrowaniem lub bez)
                links = []
                for element in link_elements:
                    href = element.get_attribute("href")
                    if href:
                        print(f"Znaleziony link: {href}")
                        if USE_FILTER:
                            if href.endswith(ALLOWED_EXTENSIONS):
                                links.append(href)
                        else:
                            links.append(href)

                # Zapisz linki do pliku
                for link in links:
                    file.write(link + "\n")

                if USE_FILTER:
                    print(f"Znaleziono {len(links)} linków z rozszerzeniami {ALLOWED_EXTENSIONS} na stronie {url}.")
                else:
                    print(f"Znaleziono {len(links)} linków na stronie {url}.")

            except Exception as e:
                print(f"Wystąpił błąd podczas przetwarzania {url}: {e}")

except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    print("Zamykanie przeglądarki...")
    if 'driver' in locals():
        driver.quit()
    print("Przeglądarka zamknięta.")