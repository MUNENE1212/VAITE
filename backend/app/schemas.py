import requests

url = "http://127.0.0.1:8000/rental/property/rent/payment"
data = {
    "tenant_name": "Munene",
    "house_number": "g",
    "amount_paid": 10000,
    "month": "February",
    "water_bill": 100,
    "electricity_bill": 200,
    "timestamp": "2025-02-19T10:17:47.758Z"
}

response = requests.post(url, json=data)
print(response.json())
