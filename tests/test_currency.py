import pandas as pd

from src.data.currency import detect_currencies


data = pd.DataFrame({
    "product": [
        "Laptop",
        "Phone",
        "Headphones",
        "Monitor"
    ],
    "price": [
        "₹50,000",
        "$800",
        "€600",
        "£400"
    ]
})


currencies = detect_currencies(data)


print("CURRENCY DETECTION")
print("------------------")

for column, detected in currencies.items():
    print(f"{column}: {detected}")