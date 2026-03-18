import re

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

products = re.findall(r'\d+\.\n(.+)', text)

price_strings = re.findall(r'\d[\d\s]*,\d{2}', text)

prices = []
for p in price_strings:
    clean = p.replace(" ", "").replace(",", ".") 
    prices.append(clean) 

total_match = re.search(r'Итого:\n([\d\s]+,\d{2})', text)

if total_match:
    total = total_match.group(1)
    total = total.replace(" ", "").replace(",", ".")
    total = float(total)
else:
    total = None

datetime_match = re.search(
    r'Время:\s*(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})',
    text
)

if datetime_match:
    datetime = datetime_match.group(1)
else:
    datetime = None

payment = None

if "Банковская карта" in text:
    payment = "Банковская карта"
elif "Наличные" in text:
    payment = "Наличные"

print("Чек:\n")

print("Товары:")
for i, p in enumerate(products, start=1):
    print(f"{i}. {p}")

print("\nЦены:")
for price in prices:
    print(price)

print("\nИтого:")
print(total)

print("\nДата и время:")
print(datetime)

print("\nСпособ оплаты:")
print(payment)