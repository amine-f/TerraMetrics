# Carboncentrik Calculator

## Overview
The Carboncentrik Calculator is a web application built using Streamlit that allows users to calculate their carbon emissions based on various factors such as transportation, electricity consumption, diet, and waste generation. The application also includes user authentication via email and stores user data in a PostgreSQL database.

## Project Structure
```
carboncentrik-calculator
├── app.py                # Main Streamlit application code
├── database              # Database related files
│   ├── __init__.py      # Initializes the database package
│   └── models.py        # Defines database models for user accounts
├── auth                  # Authentication related files
│   ├── __init__.py      # Initializes the authentication package
│   └── email_auth.py    # Handles email authentication logic
├── requirements.txt      # Lists project dependencies
├── .env                  # Contains environment variables
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd carboncentrik-calculator
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Install the required packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and add your database connection string and email service credentials:
   ```
   DATABASE_URL=your_postgresql_connection_string
   EMAIL_USER=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   ```

5. **Run the Application**
   Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Usage
- Select your country and input your daily commute distance, monthly electricity consumption, weekly waste generation, and daily meals.
- Click on "Calculate CO2 Emissions" to view your carbon footprint by category and total emissions.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.