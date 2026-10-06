from src.data.loader import load_tables
from src.data.relationship import find_possible_relationships


# Load the test tables
tables = load_tables([
    "test_data/customers.csv",
    "test_data/orders.csv"
])


# Find possible relationships
relationships = find_possible_relationships(tables)


print("POSSIBLE RELATIONSHIPS")
print("----------------------")

for relationship in relationships:
    print(relationship)