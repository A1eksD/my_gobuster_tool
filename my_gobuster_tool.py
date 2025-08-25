from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from urllib.parse import urljoin
import os, requests, re

url = "http://127.0.0.1:3000/#/"
filePath  = os.path.basename("/Desktop/gobuster_neu/wordlist.txt")
wordsFromTxt = []
foundLinks = []

# Service-Objekt anlegen
service = Service("/usr/local/bin/geckodriver")

# Firefox-Optionen
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

# WebDriver starten
driver = webdriver.Firefox(service=service, options=options)
driver.get(url)
site = driver.page_source
links = re.findall(r"https?://[^\s\"'<>]+", site)

with open(filePath) as f:
    datafile = f.readlines()

print(" --- Search for Links in the HTML")

for line in datafile:
    word = line.strip()
    for link in links:
        if word in link:
            foundLinks.append(link)

foundLinks = list(dict.fromkeys(foundLinks))
for link in foundLinks:
    print(f"found Link: {link}")

print("#####################################################")

# tokens = re.findall(r"[a-z0-9_-]+", site)
print(" --- Search for Key's in the List")


for line in datafile:
    word = re.sub(r'[^A-Za-z0-9_-]', '', line.strip())
    test_url = url + word
    
    try:
        # HEAD ist schnell; wenn der Server das nicht unterstützt, fällt er auf GET zurück
        r = requests.head(test_url, timeout=4, allow_redirects=True)
        if r.status_code >= 400:          # ungültig/404/500 …
            continue                      # überspringen
    except requests.RequestException:
        continue                          # Netzwerkfehler → auch überspringen

    # Hier nur für gültige URLs:
    print(f"Treffer: {word:20} → {test_url}")

driver.quit()
