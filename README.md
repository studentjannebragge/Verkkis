# Verkkis - Data Generation Project

## Overview

The **Verkkis** project is a Python-based data generation tool designed to simulate realistic datasets for stores, products, customers, and sales transactions. The generated data is saved in CSV format, making it suitable for analysis, testing, or other use cases.

## Features

- Generate synthetic data for:
  - Stores
  - Products
  - Customers
  - Sales transactions
- Configurable data generation parameters
- Outputs data in CSV format with customizable encoding and delimiters
- Supports Finnish locale for realistic data generation

## Requirements

The project requires the following Python libraries:

- `pandas`
- `numpy`
- `Faker`

Install the dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Configuration

The data generation parameters can be customized in the `CONFIG` dictionary within the `createData.py` script. Key parameters include:

- Number of customers, products, stores, and sales transactions
- Date ranges for sales and customer registration
- Output file names and CSV settings

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Verkkis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the data generation script:
   ```bash
   python createData.py
   ```

4. The generated CSV files will be saved in the project directory.

## Output Files

The following CSV files are generated:

- `asiakkaat.csv`: Customer data
- `tuotteet.csv`: Product data
- `myymalat.csv`: Store data
- `myynnit.csv`: Sales transaction data

## Project Structure

```
Verkkis/
├── createData.py       # Main script for data generation
├── requirements.txt    # Dependency list
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
└── Generated CSV files
```

## Development

### Adding New Features

To add new features or modify existing ones, edit the `createData.py` script. Ensure that any changes are well-documented and tested.

### Testing

Test the generated CSV files by opening them in a spreadsheet application or using Python to validate their structure and content.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or feedback, please contact the project maintainer:

- **Name**: Janne Bragge
- **Email**: [jannebragge@outlook.com]