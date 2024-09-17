import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import numpy as np

def getHeaders():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    ]
    return {'User-Agent': random.choice(user_agents), 'Accept-Language': 'en-US, en;q=0.5'}

def parse_product(product):
    try:
        name = product.h2.a.text.strip() if product.h2 and product.h2.a else np.nan
        link = "https://www.amazon.com" + product.h2.a['href'] if product.h2 and product.h2.a else np.nan
        stars = product.find('span', {'class': 'a-icon-alt'})
        stars = float(stars.text[:3].replace(",", ".")) if stars else np.nan
        num_reviews = product.find('span', {'class': 'a-size-base s-underline-text'})
        num_reviews = int(num_reviews.text.replace(",", "")) if num_reviews else np.nan
        price_whole = product.find('span', {'class': 'a-price-whole'})
        price_fraction = product.find('span', {'class': 'a-price-fraction'})
        price = float(f"{price_whole.text}.{price_fraction.text}".replace(",", "")) if price_whole and price_fraction else np.nan
        return [name, link, stars, num_reviews, price]
    except Exception as e:
        print(f"Error: {e}")
        return [np.nan] * 5

def getInfo(name, page=1, max_items=60):
    response = requests.get(f"https://www.amazon.es/s?k={name}&page={page}", headers=getHeaders())

    if response.status_code != 200:
        print(f"Código de error {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    product_list = [parse_product(product) for product in products[:max_items]]
    df = pd.DataFrame(product_list, columns=["Nombre", "Enlace", "Estrellas", "Número de Opiniones", "Precio"])
    
    return df

if __name__ == "__main__":
    df = getInfo("adios")
    print(df)
