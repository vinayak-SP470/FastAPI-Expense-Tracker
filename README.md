EXPENSE TRACKER API

This is a FastAPI-based Expense Tracker application that provides features for user authentication, expense management, and currency exchange.

Features
- User authentication (Signup, Login, JWT-based authentication)
- Expense tracking (Create, Read, Update, Delete expenses)
- Currency conversion using the ExchangeRate-API

Installation
- Python 3.10+
- PostgreSQL
- Virtual environment

Setup
1. Clone the repository:
   -> $ git clone <your-repo-url>
   -> $ cd expense_tracker
   
2. Create and activate a virtual environment:  
   -> $ python -m venv venv
   -> $ source venv/bin/activate
   
3. Install dependencies:
   -> $ pip install -r requirements.txt

4. Set up environment variables:
   Create a .env file in the root directory and add the following:
   DB_USER
   DB_PASSWORD
   DB_HOST
   DB_PORT
   DB_NAME
   EXCHANGE_RATE_API_KEY

5. Run database migrations:
   alembic upgrade head

6. Start the server:
   uvicorn app.main:app --reload

API Endpoints:

User Authentication

-Signup
http POST /users/register/

-Access Token(Login)
http POST /users/token/

-Refresh Token
http POST /users/refresh/

Expense Management
-CRUD operations

Currency Conversion
http GET /currency/convert-currency/?amount=1&from_currency=USD&to_currency=INR


