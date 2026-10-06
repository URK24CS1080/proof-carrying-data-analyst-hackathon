import pandas as pd

from src.data.units import detect_units


data = pd.DataFrame({
    "item": [
        "Rice 5 kg",
        "Sugar 500 g",
        "Water 2 L",
        "Distance 10 km",
        "Discount 20%"
    ]
})


units = detect_units(data)


print("UNIT DETECTION")
print("-------------")

for column, detected in units.items():
    print(f"{column}: {detected}")