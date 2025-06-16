"""
Converts a bank-exported CSV to a format compatible with HomeBank.
Repo: https://github.com/Outtay/simple-homebank-csv-converter

If can be run with the following arguments. If none is provided, the script will run interactively.

Args:
    input_file (str, optional): Path to the input CSV file. Defaults to None. None triggers interactive mode.
    output_file (str, optional): Path to save the output CSV file. Defaults to None. None triggers interactive mode.
    input_delimiter (str, optional): Delimiter used in the input file. Defaults to ','.
    input_separator (str, optional): Separator for the output file. Defaults to ';'.
    date_format (str, optional): Date format in the input file. Defaults to 'YYYY-MM-DD'.
    date (str, optional): Name or index of the column containing the date. Defaults to None.
    payment_type (int, optional): Payment type for all transactions. Defaults to None.
    default_payment_type (int, optional): Payment type for all transactions. Defaults to '0'.
    number (str, optional): Name or index for the column containing the number. Defaults to None.
    payee (str, optional): Name or index of the column containing the payee. Defaults to None.
    memo (str, optional): Name or index of the column containing the memo. Defaults to None.
    amount (str, optional): Name or index of the column containing the amount. Defaults to None.
    category (str, optional): Name or index of the column containing the category. Defaults to None.
    tags (str, optional): Name or index of the column containing the tags. Defaults to None.
"""

import csv
from datetime import datetime
import argparse

def show_payment_type_options():

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

def map_bank_csv_to_homebank(
                                input_file=None,
                                output_file=None,
                                input_delimiter=',',
                                input_separator=';',
                                date_format='YYYY-MM-DD',
                                date=None,
                                payment_type=None,
                                default_payment_type=0,
                                number=None,
                                payee=None,
                                memo=None,
                                amount=None,
                                category=None,
                                tags=None,
                            ):

    # HomeBank headers and descriptions
    homebank_headers = {
        "Date": "Date of the transaction (YYYY-MM-DD). Can be changed in preferences of HomeBank.",
        "Payment Type": "Type of the transaction (e.g., bank transfer, cash) with an ID used by HomeBank.",
        "Default Payment Type": "Default type of the transaction used if you did not already specify a Payment Type column.",
        "Number": "A string for cheque number, value date, card ID, transaction ID, or other details.",
        "Payee": "The recipient or originator of the transaction.",
        "Memo": "A string with notes for the transaction (e.g., reference, purpose).",
        "Amount": "The amount of the transaction (negative for expenses, positive for income).",
        "Category": "The category of the transaction.",
        "Tags": "Tags for further grouping or details about the transaction.",
    }

    # Create ouput file function
    def create_ouput_file(output_file, input_separator, date_format, payment_type, default_payment_type, homebank_headers, reader, mapping):

        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            homebank_headers_keys = list(homebank_headers.keys())
            homebank_headers_keys.remove("Default Payment Type")

            # Write headers row
            writer = csv.DictWriter(outfile, fieldnames=homebank_headers_keys, delimiter=input_separator)
            writer.writeheader()

            # Process each row in the input CSV
            for row in reader:
                output_row = {header: "" for header in homebank_headers_keys}
                for homebank_header, input_header in mapping.items():
                    if (homebank_header != "Default Payment Type") and input_header:
                        value = row[input_header]
                        # Convert date format if mapping is for the "Date" field
                        if homebank_header == "Date" and value.strip():
                            try:
                                value = datetime.strptime(value, date_format).strftime("%Y-%m-%d")
                            except ValueError:
                                print(f"Invalid date '{value}' in input file. Skipping conversion.")
                        output_row[homebank_header] = value
                if not payment_type:
                    output_row["Payment Type"] = int(default_payment_type)
                writer.writerow(output_row)
            print(f"\nHomebank CSV file successfully created at {output_file}")

    #Check params
    if input_file is None or output_file is None:

        # Interactive mode
        print(
            "This script converts a bank-exported CSV to a format compatible with HomeBank.\n"
            "Specification details can be found at: https://www.gethomebank.org/help/misc-csvformat.html\n"
        )

        input_file = input("Enter the path to the input CSV file: ")
        output_file = input("Enter the path to save the output CSV file: ")

        input_delimiter = input("Enter the delimiter used in the input file (default is ','): ") or input_delimiter
        input_separator = input("Enter the separator for the output file (default is ';'): ") or input_separator

        # Ask for input date format
        date_format = input("Enter the date format in the input file (default is 'YYYY-MM-DD'): ") or date_format
        date_format = date_format.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y")


        # Read the input CSV to get headers
        try:
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
                    if homebank_header != "Default Payment Type":
                        print(f"\nHomeBank Field: {homebank_header}")
                        print(f"Description: {description}")
                        print("Available columns in input file:")
                        for idx, col in enumerate(input_headers):
                            example = examples[col] if examples[col].strip() else "<empty>"
                            print(f"{idx + 1}: {col} (Example: {example})")
                        choice = input(f"Enter the column number to map to '{homebank_header}' or press Enter to leave it empty: ")
                        homebank_header = homebank_header.replace(' ', '_')
                        if choice.isdigit() and 1 <= int(choice) <= len(input_headers):
                            mapping[homebank_header] = input_headers[int(choice) - 1]
                        else:
                            mapping[homebank_header] = None

                # Handle 'Default Payment Type' field interactively
                if not payment_type:
                    print("\nThe payment Type field is required by HomeBank. Set a default type to apply to all lines:")
                    show_payment_type_options()
                    default_payment_type = input("Enter Payment Type for all transactions (default is '0 = none'): ") or default_payment_type
                    while default_payment_type not in payment_type_mapping:
                        default_payment_type = input("Invalid input. Enter a valid Payment Type: ")

                    create_ouput_file(output_file, input_separator, date_format, payment_type, default_payment_type, homebank_headers, reader, mapping)

        except FileNotFoundError:
            print(f"\nError: Input file not found: {input_file}")
            return
        except ValueError as e:
            print(f"\nError: {e}")
            return

    else:
        # Non-interactive mode (from params)
        date_format = date_format.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y")

        # Read the input CSV
        try:
            with open(input_file, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile, delimiter=input_delimiter)
                input_headers = reader.fieldnames

                if not input_headers:
                    raise ValueError("Input file has no headers.")

                args_list=locals()
                mapping = {}
                for homebank_header, description in homebank_headers.items():
                    key = homebank_header.lower().replace(' ', '_')
                    choice = args_list[key]
                    if choice and choice.isdigit() and 1 <= int(choice) <= len(input_headers):
                        mapping[homebank_header] = input_headers[int(choice)-1]
                    else:
                        mapping[homebank_header] = None

                create_ouput_file(output_file, input_separator, date_format, payment_type, default_payment_type, homebank_headers, reader, mapping)

        except FileNotFoundError:
            print(f"\nError: Input file not found: {input_file}")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert bank CSV to HomeBank format.  Run without arguments for interactive mode.")
    parser.add_argument("input_file", nargs='?', help="Path to the input CSV file.")
    parser.add_argument("output_file", nargs='?', help="Path to save the output CSV file.")
    parser.add_argument("--input_delimiter", default=",", help="Delimiter used in the input file (default: ,).")
    parser.add_argument("--input_separator", default=";", help="Separator for the output file (default: ;).")
    parser.add_argument("--date_format", default="YYYY-MM-DD", help="Date format in the input file (default: YYYY-MM-DD).")
    parser.add_argument("--date", help="(int) Index of the column containing the date.")
    parser.add_argument("--payment_type", help="(int) Index of the column containing the payment type.")
    parser.add_argument("--default_payment_type", default="0", help="Defaut payment type for all transactions, used if no payment type column has been specified (default: 0).")
    parser.add_argument("--number", help="(int) Index of the column containing the cheque number, value date, card ID, transaction ID, or other details.")
    parser.add_argument("--payee", help="(int) Index of the column containing the payee.")
    parser.add_argument("--memo", help="(int) Index of the column containing the memo.")
    parser.add_argument("--amount", help="(int) Index of the column containing the amount.")
    parser.add_argument("--category", help="(int) Index of the column containing the category.")
    parser.add_argument("--tags", help="(int) Index of the column containing the tags.")

    args = parser.parse_args()

    if args.default_payment_type:
        allowed_range = list(range(10))
        allowed_range.remove(5)
        if int(args.default_payment_type) not in allowed_range:
            print('\nInvalid Default Payment Type value. Try with an integer from the list below:\n')
            show_payment_type_options()
            exit()

    map_bank_csv_to_homebank(
                                args.input_file,
                                args.output_file,
                                args.input_delimiter,
                                args.input_separator,
                                args.date_format,
                                args.date,
                                args.payment_type,
                                args.default_payment_type,
                                args.number,
                                args.payee,
                                args.memo,
                                args.amount,
                                args.category,
                                args.tags
                            )
