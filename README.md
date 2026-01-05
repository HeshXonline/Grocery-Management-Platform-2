# Grocery Shop Management System

A complete local web application for managing a small grocery shop's inventory, sales, and reports.

## Tech Stack
- **Backend**: Python FastAPI + SQLAlchemy
- **Database**: MySQL
- **Frontend**: HTML + CSS + JavaScript (Vanilla)

## Features
- Product inventory management
- Point of sale / Billing system
- Live daily business metrics
- Comprehensive reports (revenue, profit, stock)

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL Server installed and running
- pip (Python package manager)

### 2. Database Setup

Create the MySQL database:
```sql
CREATE DATABASE grocery_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Database Connection

Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

Edit `.env` and update with your MySQL credentials:
```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/grocery_db
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize Database Tables
```bash
python init_db.py
```

### 6. (Optional) Load Sample Data
```bash
python sample_data.py
```

### 7. Start the Application
```bash
python main.py
```

The application will start at: **http://localhost:8000**

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
