## Forex Currency Converter Application

This project is a **Forex Currency Converter** web application built with Flask. It allows users to convert currencies, view currency tables, and conduct conversions between various currency pairs.

### Table of Contents
- [Forex Currency Converter Application](#forex-currency-converter-application)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps to Install](#steps-to-install)
  - [Running the Application](#running-the-application)
  - [Configuration](#configuration)
  - [Running Tests](#running-tests)
  - [Technologies Used](#technologies-used)
  - [License](#license)
  - [Contributing](#contributing)
  - [Contact](#contact)
  - [Acknowledgments](#acknowledgments)

---

### Project Overview

The **Forex Currency Converter** web application provides a simple interface for users to:
- Convert amounts between two currencies.
- View conversion results and historical exchange rates.
- Display currency tables for quick reference.

### Installation

#### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- Virtualenv (optional but recommended)

#### Steps to Install

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/forex-converter.git
    cd forex-converter
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Run the Flask development server**:
    ```bash
    flask run
    ```

2. Open your browser and navigate to `http://localhost:5000` to access the app.

### Configuration

You can modify application settings by updating the `config.py` or directly within `app.py`. Ensure that the following configuration variables are set properly:

- `DEBUG_TB_INTERCEPT_REDIRECTS = False`: This ensures that the Flask Debug Toolbar doesn't interfere with redirects during testing.

### Running Tests

This application includes unit tests to ensure proper functionality. Tests are located in the `test_app.py` file and are built using the `unittest` module.

To run the tests:

1. **Run tests**:
    ```bash
    python -m unittest test_app.py
    ```

2. **Test Coverage**:
    - The tests cover different routes like `/`, `/convert`, and `/table`.
    - Tests validate that redirects occur correctly and that the proper content is rendered on the pages.

### Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **Flask-DebugToolbar**: Provides a set of debug tools for Flask applications.
- **Flask-Testing**: Used for unit testing Flask applications.
- **forex-python**: For fetching real-time exchange rates and performing currency conversions.
- **Unittest**: A built-in Python library used to write and run tests.

---

### License
This project is licensed under the MIT License.

---

### Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Open a pull request with detailed changes.

---

### Contact

If you have any questions or need help, feel free to reach out at `brice.web.development@gmail.com`.

---

### Acknowledgments

Special thanks to everyone who contributed to open-source libraries used in this project.
