Apologies for the confusion earlier. Here's an updated README file template:

# Tax Tracking System

The Tax Tracking System is a Python application that allows citizens to track and pay their taxes. It provides features for citizens to view their tax details, pay personal and business taxes, and check their tax payment history. The system also includes an administrator interface to manage citizen information, view tax details of all citizens, and generate reports.

## Features

- Citizens can:
  - View their personal information and tax details
  - Pay personal and business taxes
  - View their tax payment history

- Administrator can:
  - Search for a citizen by ID
  - Find citizens working for a specific employer
  - Retrieve tax details of all citizens
  - Get data on citizens with paid taxes (in descending order of total tax paid)
  - Register new citizens
  - Calculate total tax paid by all citizens
  - View citizens with pending tax settlements

## Technologies Used

- Python
- SQLAlchemy (Object-Relational Mapping)
- SQLite (Database)

## Setup and Usage

1. Install the required dependencies:

```
pip install sqlalchemy
```

2. Clone the repository:

```
git clone https://github.com/your-username/tax-tracking-system.git
```

3. Navigate to the project directory:

```
cd tax-tracking-system
```

4. Run the `populate_database` function to create and populate the database with sample data:

```python
python -c "from main import populate_database; populate_database()"
```

5. Run the application:

```python
python main.py
```

6. Follow the on-screen prompts to navigate through the application.

## Database Schema

The application uses an SQLite database to store citizen information and tax details. The database schema consists of the following tables:

- `citizens`: Stores citizen information (ID, first name, last name, profession, employer, salary, business income, total income).
- `tax_details`: Stores tax details for each citizen (ID, citizen ID, first name, last name, paye, housing levy, road levy, service fee, business tax, total tax).
- `taxes_paid`: Stores tax payment information for each citizen (ID, citizen ID, personal tax paid, business tax paid, total tax paid, taxes left to pay, Mpesa code).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributors

- [Bethwel Kipruto Kangogo](https://github.com/bethwelkipruto)

Feel free to contribute to the project by submitting bug reports, feature requests, or pull requests.