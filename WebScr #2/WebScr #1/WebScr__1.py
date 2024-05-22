import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = [title.text.strip() for title in soup.find_all('div', class_='title')][:10]
    prices_raw = [price.text for price in soup.find_all('b', class_='orangeText')][:10]

    cleaned_prices = []
    for price_tag in prices_raw:
        price_str = price_tag
        cleaned_price = re.sub(r'[^\d.]', '', price_str)
        try:
            price = float(cleaned_price) * 1000
            cleaned_prices.append(price)
        except ValueError:
            cleaned_prices.append(0.0)

    return titles, cleaned_prices

def get_car_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        return parse_data(response.content)
    else:
        print(f"Failed to fetch {url}")
        return [], []

def scrape_parallel(urls):
    car_info_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_car_info, url) for url in urls]
        for future in futures:
            car_info = future.result()
            if car_info:
                car_info_list.append(car_info)
    return car_info_list

base_url = "https://www.tiriacauto.ro/auto-rulate"
urls = [f"{base_url}?page={page}" for page in range(1, 6)]

car_data = scrape_parallel(urls)

doc = SimpleDocTemplate("output.pdf", pagesize=letter)
styles = getSampleStyleSheet()
title_style = styles["Heading1"]
normal_style = styles["Normal"]

content = []

for titles, prices in car_data:
    for title, price in zip(titles, prices):
        content.append(Paragraph(f"Title: {title}, Price: {price}", normal_style))

all_prices = [price for _, prices in car_data for price in prices]
content.append(Paragraph(f"Masina cea mai scumpa: {car_data[all_prices.index(max(all_prices)) // 10][0][all_prices.index(max(all_prices)) % 10]}, Price: {max(all_prices):.2f} €", normal_style))
content.append(Paragraph(f"Masina cea mai ieftina: {car_data[all_prices.index(min(all_prices)) // 10][0][all_prices.index(min(all_prices)) % 10]}, Price: {min(all_prices):.2f} €", normal_style))
content.append(Paragraph(f"Media preturilor: {sum(all_prices) / len(all_prices):.2f} €", normal_style))
content.append(Paragraph(f"Numarul total de masini: {len(all_prices)}", normal_style))
content.append(Paragraph(f"Pretul maxim: {max(all_prices):.2f} €", normal_style))
content.append(Paragraph(f"Pretul minim: {min(all_prices):.2f} €", normal_style))

plt.figure(figsize=(10, 6))
plt.bar(range(len(all_prices)), sorted(all_prices))
plt.xlabel('Mașini')
plt.ylabel('Preț (€)')
plt.title('Prețul mașinilor de la cea mai ieftină la cea mai scumpă')
plt.xticks(range(len(all_prices)), [car_data[i // 10][0][i % 10] for i in range(len(all_prices))], rotation=90)
plt.tight_layout()

plt.savefig('cars_prices_chart.pdf')

plt.show()

doc.build(content)
print("Datele au fost scrise cu succes în fișierul 'output.pdf', iar graficul a fost salvat în fișierul 'cars_prices_chart.pdf'.")
