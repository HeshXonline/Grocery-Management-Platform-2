# Grocery Shop Management System

A complete local web application for managing a small grocery shop's inventory, sales, and reports.

## Tech Stack
- **Backend**: Python FastAPI + SQLAlchemy
- **Database**: SQLite (default) or MySQL
- **Frontend**: HTML + CSS + JavaScript (Vanilla)

## Features
- Product inventory management
- Point of sale / Billing system
- Live daily business metrics
- Comprehensive reports (revenue, profit, stock)
- Add, edit, delete products
- Stock-based profit forecasting

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Database

The application uses SQLite by default (no installation needed).

**Option A: SQLite (Default - Recommended)**
```bash
# Database will be created automatically as grocery.db
python init_db.py
```

**Option B: MySQL (Optional)**
```bash
# First, create MySQL database:
# CREATE DATABASE grocery_db;

# Then update .env file:
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/grocery_db

# Run initialization:
python init_db.py
```

### 4. Load Sample Data (Optional)
```bash
python sample_data.py
```

### 5. Start the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will start at: **http://localhost:8000**

## 🌐 Cloud Deployment

### PythonAnywhere (Free Hosting)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete step-by-step instructions.

**Quick Steps:**
1. Clone repository on PythonAnywhere
2. Run `bash setup_pythonanywhere.sh`
3. Configure WSGI file
4. Set up static files mapping
5. Reload web app

Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

## Application Pages

- **Dashboard** (`/`) - View daily metrics and transactions
- **Billing** (`/billing.html`) - Create sales and manage transactions
- **Reports** (`/reports.html`) - View all-time reports and stock levels

## API Documentation

Once running, visit: **http://localhost:8000/docs**

## Database Schema

### products
- Stores product information, pricing, and stock levels

### sales
- Records each sale transaction with total amount and profit

### sale_items
- Individual line items for each sale with quantity and prices

## Usage Guide

### Adding Products
Use the API directly or add products via Python script.

### Making a Sale
1. Go to Billing page
2. Select products and quantities
3. Complete the sale
4. Stock automatically reduces

### Viewing Metrics
- Dashboard shows today's performance
- Reports page shows all-time data and current stock

## Important Notes
- This is a LOCAL application (single computer use)
- No authentication required
- No cloud/online features
- All data stored in local MySQL database

## Support
For issues or questions, check the API documentation at `/docs` endpoint.
