import csv
from datetime import datetime

def map_bank_csv_to_homebank(input_file, output_file):
    print(
        "This script converts a bank-exported CSV to a format compatible with HomeBank.\n"
        "Specification details can be found at: https://www.gethomebank.org/help/misc-csvformat.html\n"
    )

    # HomeBank headers and descriptions
    homebank_headers = {
        "Date": "Date of the transaction (YYYY-MM-DD). Can be changed in preferences of HomeBank.",
        "Payment": "Type of the transaction (e.g., bank transfer, cash) with an ID used by HomeBank.",
        "Number": "A string for cheque number, value date, card ID, transaction ID, or other details.",
        "Payee": "The recipient or originator of the transaction.",
        "Memo": "A string with notes for the transaction (e.g., reference, purpose).",
        "Amount": "The amount of the transaction (negative for expenses, positive for income).",
        "Category": "The category of the transaction.",
        "Tags": "Tags for further grouping or details about the transaction.",
    }

    input_delimiter = input("Enter the delimiter used in the input file (default is ','): ") or ","
    separator = input("Enter the separator for the output file (default is ';'): ") or ";"

    # Ask for input date format
    input_date_format = input("Enter the date format in the input file (default is 'YYYY-MM-DD'): ") or "YYYY-MM-DD"
    input_date_format = input_date_format.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y")

    # Read the input CSV
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=input_delimiter)
        input_headers = reader.fieldnames
        if not input_headers:
            raise ValueError("Input file has no headers.")

        # Preview for first non-empty example
        first_row = next(reader)
        examples = {header: first_row[header] for header in input_headers}
        infile.seek(0)  # Reset reader to start
        next(reader)  # Skip header row

        # Create a mapping dictionary
        mapping = {}
        for homebank_header, description in homebank_headers.items():
            if homebank_header != "Payment":
                print(f"\nHomeBank Field: {homebank_header}")
                print(f"Description: {description}")
                print("Available columns in input file:")
                for idx, col in enumerate(input_headers):
                    example = examples[col] if examples[col].strip() else "<empty>"
                    print(f"{idx + 1}: {col} (Example: {example})")
                choice = input(f"Enter the column number to map to '{homebank_header}' or press Enter to leave it empty: ")
                if choice.isdigit() and 1 <= int(choice) <= len(input_headers):
                    mapping[homebank_header] = input_headers[int(choice) - 1]
                else:
                    mapping[homebank_header] = None

        # Handle 'Payment' field
        print("\nPayment field requires a type for all lines:")
        payment_type_mapping = {
            "0": "none",
            "1": "credit card",
            "2": "check",
            "3": "cash",
            "4": "bank transfer",
            "6": "debit card",
            "7": "standing order",
            "8": "electronic payment",
            "9": "deposit",
            "10": "financial institution fee",
            "11": "direct debit",
        }
        print("Payment Type Options:")
        for key, val in payment_type_mapping.items():
            print(f"{key} = {val}")
        payment_type = input("Enter Payment type for all transactions (default is '0 = none'): ") or "0"
        while payment_type not in payment_type_mapping:
            payment_type = input("Invalid input. Enter a valid Payment type: ")

        # Open the output CSV
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=homebank_headers.keys(), delimiter=separator)
            writer.writeheader()

            # Process each row in the input CSV
            for row in reader:
                output_row = {header: "" for header in homebank_headers.keys()}
                for homebank_header, input_header in mapping.items():
                    if input_header:
                        value = row[input_header]
                        # Convert date format if mapping is for the "Date" field
                        if homebank_header == "Date" and value.strip():
                            try:
                                value = datetime.strptime(value, input_date_format).strftime("%Y-%m-%d")
                            except ValueError:
                                print(f"Invalid date '{value}' in input file. Skipping conversion.")
                        output_row[homebank_header] = value

                output_row["Payment"] = payment_type
                writer.writerow(output_row)

if __name__ == "__main__":
    input_csv = input("Enter the path to the input CSV file: ")
    output_csv = input("Enter the path to save the output CSV file: ")
    map_bank_csv_to_homebank(input_csv, output_csv)
