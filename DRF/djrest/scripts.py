import os
import csv
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djrest.settings")
django.setup()

from products.models import Product  
import random

def load_data_from_csv(file_path):
    """
    Load product data from a CSV file and insert it into the Product model.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            products = []

            for row in reader:
                product_name = row.get('product_name')
                product_brand = row.get('product_brand')

                if not product_name or not product_brand:
                    print(f"Skipping row with missing data: {row}")
                    continue

                products.append(Product(
                    product_name=product_name,
                    product_brand=product_brand,
                    product_price = random.uniform(100, 10000)
                    ))

            Product.objects.bulk_create(products)
            print(f"Successfully uploaded {len(products)} products.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    csv_file_path = "MOCK_DATA.csv"  
    load_data_from_csv(csv_file_path)
