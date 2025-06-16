# simple-homebank-csv-converter
Simple python script to convert a csv into the format homebank expects either interactively or by passing CLI parameters

## Motivation
- Neither of my banks offers export into QIF or QFX exports
- All existing solutions are tailored to specific bank exports, meaning for an unsupported bank I'd have to create an issue or script it myself anyway
- Homebank gives no feedback if the csv is not correct, which made first attempts with LibreOffice cumbersome

## How it works
The script is extremely simple, if you just want to get your transactions somehow into Homebank.
It's interactive and asks what existing columns you want to map onto the columns that Homebank expects.
The only "extras" are that it converts the date format into the format expected by Homebank and adds a payment_type column with a default value in the case that you don't have such column defined.

Note: For Raiffeisen I had to add a header row. Not sure if it would work without it, but it made it easier to map the columns.

## Usage
### Interactive mode
`python homeBankCSVConverter.py`

### CLI mode
Pass some or all of the parameters described below and the script won't prompt for any interaction.

Example: `python homeBankCSVConverter.py "/path/to/input_file" "path/to/output_file" --date=2 --amount=4 --memo=5`

Required:
|   Parameter   |  Type  |  Description |
| ------------- | ------ | ------------ |
| `input_file`  | string | Path to the input CSV file |
| `output_file` | string | Path to save the output CSV file |

Optional:
|   Parameter               |  Type   |  Description      | Default value |
| ------------------------- | ------- | ----------------- | ------------- |
| `-h`, `--help`            |         | Show help message |               |
| `--input_delimiter`       | string  | Delimiter used in the input file  | `,` |
| `--input_separator`       | string  | Separator for the output file  | `;` |
| `--date_format`           | string  | Date format in the input file  | `YYYY-MM-DD` |
| `--date`                  | integer | Index of the column containing the date | `None` |
| `--payment_type`          | integer | Index of the column containing the payment type | `None` |
| `--default_payment_type`  | integer | Defaut payment type for all transactions, used if no payment type column has been specified  | `0` |
| `--number`                | integer | Index of the column containing the cheque number, value date, card ID, transaction ID, or other details | `None` |
| `--payee`                 | integer | Index of the column containing the payee | `None` |
| `--memo`                  | integer | Index of the column containing the memo | `None` |
| `--amount`                | integer | Index of the column containing the amount | `None` |
| `--category`              | integer | Index of the column containing the category | `None` |
| `--tags`                  | integer | Index of the column containing the tags | `None` |


## Reference Link
https://www.gethomebank.org/help/misc-csvformat.html
