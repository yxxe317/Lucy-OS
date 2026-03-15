import httpx
from bs4 import BeautifulSoup

response = httpx.get('https://example.com')
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title.string)