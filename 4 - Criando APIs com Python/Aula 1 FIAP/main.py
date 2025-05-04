import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://exemplo.com'
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
else:
    print(f"Erro {response.status_code}")


