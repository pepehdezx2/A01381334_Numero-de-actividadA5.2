import json
import sys
import time


def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' contains invalid JSON.")
        return None


def compute_total_sales(price_catalog, sales_record):
    """Compute total sales based on price catalog and sales records."""
    total_sales = 0
    errors = []
    
    for sale in sales_record:
        product = sale.get("product")
        quantity = sale.get("quantity")

        if product is None or quantity is None:
            errors.append(f"Invalid entry: {sale}")
            continue
        
        price = price_catalog.get(product)
        if price is None:
            errors.append(f"Error: Product '{product}' not found in price catalog.")
            continue

        try:
            total_sales += price * quantity
        except TypeError:
            errors.append(f"Invalid quantity or price for product '{product}'.")
    
    return total_sales, errors


def main():
    """Main function to handle the sales computation."""
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_catalog_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    # Load JSON files
    price_catalog = load_json(price_catalog_file)
    sales_record = load_json(sales_record_file)

    if price_catalog is None or sales_record is None:
        sys.exit(1)

    start_time = time.time()

    # Compute total sales
    total_sales, errors = compute_total_sales(price_catalog, sales_record)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Display results
    print(f"Total Sales: ${total_sales:.2f}")
    print(f"Execution Time: {elapsed_time:.4f} seconds")

    # Save to file
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(f"Total Sales: ${total_sales:.2f}\n")
        result_file.write(f"Execution Time: {elapsed_time:.4f} seconds\n")
        if errors:
            result_file.write("\nErrors:\n" + "\n".join(errors))

    # Print errors to console
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(error)


if __name__ == "__main__":
    main()
