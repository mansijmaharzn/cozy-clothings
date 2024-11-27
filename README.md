# Cozy Clothings 🧥

Welcome to **Cozy Clothings**, an e-commerce project built with Django. This guide will walk you through the steps to clone the repository, set up the environment, and run the project locally.

## Prerequisites

Ensure you have the following installed:

- **Python** (>= 3.8)
- **pip** (Python package manager)
- **Git**

## Quick Start

Run the following commands in sequence to set up and start the project:

### 1. Clone the Repository

```bash
git clone https://github.com/mansijmaharzn/cozy-clothings.git
cd cozy-clothings
```

### 2. Create and Activate a Virtual Environment

- For Linux/MacOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

- For Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. Access the Application
Open your browser and visit: http://127.0.0.1:8000/
---