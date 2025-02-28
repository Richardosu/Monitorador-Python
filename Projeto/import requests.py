import requests
from bs4 import BeautifulSoup
import re

url = "https://a.co/d/6X9WWP7"  

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    
    title = soup.find("span", {"id": "productTitle"})
    title = title.text.strip() if title else "Produto não encontrado"
    
    
    price = soup.find("span", class_=re.compile("a-price-whole"))
    price = price.text.strip() if price else "Preço não encontrado"
    
    print(f"Produto: {title}")
    print(f"Preço: R$ {price}")
else:
    print("Erro ao acessar a página.")