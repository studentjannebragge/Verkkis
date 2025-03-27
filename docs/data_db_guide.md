# **data.db** - SQLite Database Guide

## Overview

The `data.db` file is an SQLite database that stores the data generated from the CSV files. This database is created and populated using the `load_csv_to_sqlite.py` script. It provides a structured way to query and analyze the data.

## How to Use

### 1. **Generate the Database**

To create and populate the `data.db` database:

1. Ensure the required CSV files (`asiakkaat.csv`, `tuotteet.csv`, `myymalat.csv`, `myynnit.csv`) are located in the `data/` directory.
2. Run the `load_csv_to_sqlite.py` script:
   ```bash
   python load_csv_to_sqlite.py
   ```
3. The `data.db` file will be created in the project directory.

### 2. **Query the Database**

You can query the `data.db` database using any SQLite-compatible tool or library. Examples include:

- **SQLite CLI**:
  ```bash
  sqlite3 data.db
  ```
  Example query:
  ```sql
  SELECT * FROM asiakkaat LIMIT 10;
  ```

- **Python**:
  ```python
  import sqlite3

  conn = sqlite3.connect("data.db")
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM asiakkaat LIMIT 10")
  rows = cursor.fetchall()

  for row in rows:
      print(row)

  conn.close()
  ```

- **GUI Tools**:
  Use tools like [DB Browser for SQLite](https://sqlitebrowser.org/) to open and explore the database.

### 3. **Database Tables**

The database contains the following tables:

- **`asiakkaat`**: Customer data
  - Columns: `AsiakasID`, `Etunimi`, `Sukunimi`, `Sahkoposti`, `Puhelinnumero`, `Kaupunki`, `Rekisteroitymispaiva`

- **`tuotteet`**: Product data
  - Columns: `TuoteID`, `Tuotenimi`, `Kategoria`, `Yksikkohinta`, `Kuvaus`

- **`myymalat`**: Store data
  - Columns: `MyymalaID`, `MyymalanNimi`, `Kaupunki`, `Alue`, `Osoite`

- **`myynnit`**: Sales transaction data
  - Columns: `TapahtumaID`, `Pvm`, `AsiakasID`, `TuoteID`, `MyymalaID`, `Maara`, `Yksikkohinta`, `Kokonaishinta`, `Maksutapa`

### 4. **Modify or Extend the Database**

If you need to modify or extend the database schema:

1. Open the `load_csv_to_sqlite.py` script.
2. Add or modify the logic for creating tables or loading data.
3. Rerun the script to apply changes.

### 5. **Backup and Exclude from Version Control**

To avoid accidental loss of data:

- Backup the `data.db` file regularly.
- Ensure the `data.db` file is excluded from version control by adding it to `.gitignore` (already configured).

## Troubleshooting

- **Missing Tables**: Ensure the CSV files are correctly formatted and located in the `data/` directory.
- **Database Locked**: Close any other applications accessing the `data.db` file and try again.
- **Corrupted Database**: Delete the `data.db` file and rerun the `load_csv_to_sqlite.py` script to regenerate it.

## Additional Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
