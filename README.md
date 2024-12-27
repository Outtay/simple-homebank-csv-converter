# simple-homebank-csv-converter
Simple python script to interactively convert a csv into the format homebank expects

## Motivation
- Neither of my banks offers export into QIF or QFX exports
- All existing solutions are tailored to specific bank exports, meaning for an unsupported bank I'd have to create an issue or script it myself anyway
- Homebank gives no feedback if the csv is not correct, which made first attempts with LibreOffice cumbersome

## How it works
The script is extremely simple, if you just want to get your transactions somehow into Homebank.  
It's interactive and asks what existing columns you want to map onto the columns that Homebank expects.  
The only "extra" is that it can convert date formats into the format expected from Homebank.

Note: For Raiffeisen I had to add a header row. Not sure if it would work without it, but it made it easier to map the columns.

## Usage
`python homeBankCSVConverter.py`

## Reference Link
https://www.gethomebank.org/help/misc-csvformat.html
