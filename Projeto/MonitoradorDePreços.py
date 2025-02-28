import requests
from bs4 import BeautifulSoup
import sqlite3
import smtplib
import time
import re
import pandas as pd

# Configurações
URL = "https://a.co/d/6X9WWP7"  
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
ALERT_PRICE = 400  
EMAIL = ""  
PASSWORD = ""  

def get_price():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("span", {"id": "productTitle"})
        title = title.text.strip() if title else "Produto não encontrado"
        price = soup.find("span", class_=re.compile("a-price-whole"))
        price = int(price.text.replace('.', '').strip()) if price else None
        return title, price
    return None, None

def save_price(title, price):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            price INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("INSERT INTO prices (product, price) VALUES (?, ?)", (title, price))
    conn.commit()
    conn.close()

def check_price_drop(price):
    if price and price <= ALERT_PRICE:
        send_email(price)

def send_email(price):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        subject = "Alerta de Preço Baixo!"
        body = f"O produto está por R$ {price}. Confira: {URL}"
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL, EMAIL, msg)
        print("Email enviado!")

def show_price_history():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product, price, date FROM prices ORDER BY date DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(rows, columns=["Produto", "Preço", "Data"])
    print(df)
    
    df.to_csv("historico_precos.csv", index=False)
    print("Histórico de preços salvo em 'historico_precos.csv'")

if __name__ == "__main__":
    while True:
        title, price = get_price()
        if title and price:
            print(f"Produto: {title} - Preço: R$ {price}")
            save_price(title, price)
            check_price_drop(price)
            show_price_history()
        time.sleep(3600)
