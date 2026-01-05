from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
import uvicorn

from config import get_db, engine, Base
from models import Product, Sale, SaleItem

# Create FastAPI app
app = FastAPI(title="Grocery Shop Management System", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== Pydantic Schemas ====================

class ProductCreate(BaseModel):
    name: str
    category: str
    buying_price: float
    selling_price: float
    stock_quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    buying_price: float
    selling_price: float
    stock_quantity: int
    created_at: datetime

    class Config:
        from_attributes = True

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    items: List[SaleItemCreate]

class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    selling_price: float
    buying_price: float

class SaleResponse(BaseModel):
    id: int
    total_amount: float
    profit: float
    created_at: datetime
    items: List[SaleItemResponse]

class DashboardStats(BaseModel):
    daily_transactions: int
    daily_revenue: float
    daily_profit: float

class ReportStats(BaseModel):
    total_revenue: float
    total_profit: float
    total_transactions: int

class StockItem(BaseModel):
    product_id: int
    product_name: str
    category: str
    stock_quantity: int
    buying_price: float
    selling_price: float

# ==================== Product APIs ====================

@app.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    db_product = Product(
        name=product.name,
        category=product.category,
        buying_price=product.buying_price,
        selling_price=product.selling_price,
        stock_quantity=product.stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(Product).order_by(Product.name).all()
    return products

@app.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.name = product.name
    db_product.category = product.category
    db_product.buying_price = product.buying_price
    db_product.selling_price = product.selling_price
    db_product.stock_quantity = product.stock_quantity
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product has been sold
    sale_items_count = db.query(SaleItem).filter(SaleItem.product_id == product_id).count()
    if sale_items_count > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete product that has sales history. Consider setting stock to 0 instead."
        )
    
    db.delete(db_product)
    db.commit()
    return None

# ==================== Sales / Billing APIs ====================

@app.post("/api/sales", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db)):
    """Create a new sale transaction"""
    if not sale_data.items:
        raise HTTPException(status_code=400, detail="Sale must have at least one item")
    
    total_amount = 0.0
    total_profit = 0.0
    sale_items_list = []
    
    # Validate and calculate totals
    for item in sale_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for {product.name}. Available: {product.stock_quantity}"
            )
        
        item_total = product.selling_price * item.quantity
        item_cost = product.buying_price * item.quantity
        item_profit = item_total - item_cost
        
        total_amount += item_total
        total_profit += item_profit
        
        sale_items_list.append({
            "product": product,
            "quantity": item.quantity,
            "selling_price": product.selling_price,
            "buying_price": product.buying_price
        })
    
    # Create sale
    db_sale = Sale(
        total_amount=total_amount,
        profit=total_profit
    )
    db.add(db_sale)
    db.flush()  # Get sale ID
    
    # Create sale items and update stock
    response_items = []
    for item_data in sale_items_list:
        sale_item = SaleItem(
            sale_id=db_sale.id,
            product_id=item_data["product"].id,
            quantity=item_data["quantity"],
            selling_price=item_data["selling_price"],
            buying_price=item_data["buying_price"]
        )
        db.add(sale_item)
        
        # Reduce stock
        item_data["product"].stock_quantity -= item_data["quantity"]
        
        response_items.append({
            "id": sale_item.id,
            "product_id": item_data["product"].id,
            "product_name": item_data["product"].name,
            "quantity": item_data["quantity"],
            "selling_price": item_data["selling_price"],
            "buying_price": item_data["buying_price"]
        })
    
    db.commit()
    db.refresh(db_sale)
    
    return {
        "id": db_sale.id,
        "total_amount": db_sale.total_amount,
        "profit": db_sale.profit,
        "created_at": db_sale.created_at,
        "items": response_items
    }

@app.get("/api/sales", response_model=List[SaleResponse])
def get_all_sales(limit: int = 100, db: Session = Depends(get_db)):
    """Get all sales"""
    sales = db.query(Sale).order_by(Sale.created_at.desc()).limit(limit).all()
    
    result = []
    for sale in sales:
        items = []
        for sale_item in sale.sale_items:
            items.append({
                "id": sale_item.id,
                "product_id": sale_item.product_id,
                "product_name": sale_item.product.name,
                "quantity": sale_item.quantity,
                "selling_price": sale_item.selling_price,
                "buying_price": sale_item.buying_price
            })
        
        result.append({
            "id": sale.id,
            "total_amount": sale.total_amount,
            "profit": sale.profit,
            "created_at": sale.created_at,
            "items": items
        })
    
    return result

# ==================== Dashboard APIs ====================

@app.get("/api/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get today's dashboard statistics"""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    # Query today's sales
    today_sales = db.query(Sale).filter(
        and_(
            Sale.created_at >= today_start,
            Sale.created_at <= today_end
        )
    ).all()
    
    daily_transactions = len(today_sales)
    daily_revenue = sum(sale.total_amount for sale in today_sales)
    daily_profit = sum(sale.profit for sale in today_sales)
    
    return {
        "daily_transactions": daily_transactions,
        "daily_revenue": daily_revenue,
        "daily_profit": daily_profit
    }

@app.get("/api/dashboard/today-transactions", response_model=List[SaleResponse])
def get_today_transactions(db: Session = Depends(get_db)):
    """Get today's transactions"""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    sales = db.query(Sale).filter(
        and_(
            Sale.created_at >= today_start,
            Sale.created_at <= today_end
        )
    ).order_by(Sale.created_at.desc()).all()
    
    result = []
    for sale in sales:
        items = []
        for sale_item in sale.sale_items:
            items.append({
                "id": sale_item.id,
                "product_id": sale_item.product_id,
                "product_name": sale_item.product.name,
                "quantity": sale_item.quantity,
                "selling_price": sale_item.selling_price,
                "buying_price": sale_item.buying_price
            })
        
        result.append({
            "id": sale.id,
            "total_amount": sale.total_amount,
            "profit": sale.profit,
            "created_at": sale.created_at,
            "items": items
        })
    
    return result

# ==================== Reports APIs ====================

@app.get("/api/reports/summary", response_model=ReportStats)
def get_reports_summary(db: Session = Depends(get_db)):
    """Get all-time reports summary"""
    sales = db.query(Sale).all()
    
    total_revenue = sum(sale.total_amount for sale in sales)
    total_profit = sum(sale.profit for sale in sales)
    total_transactions = len(sales)
    
    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_transactions": total_transactions
    }

@app.get("/api/reports/stock", response_model=List[StockItem])
def get_stock_report(db: Session = Depends(get_db)):
    """Get current stock levels for all products"""
    products = db.query(Product).order_by(Product.category, Product.name).all()
    
    result = []
    for product in products:
        result.append({
            "product_id": product.id,
            "product_name": product.name,
            "category": product.category,
            "stock_quantity": product.stock_quantity,
            "buying_price": product.buying_price,
            "selling_price": product.selling_price
        })
    
    return result

# ==================== Frontend Routes ====================

@app.get("/")
def serve_dashboard():
    """Serve dashboard page"""
    return FileResponse("static/index.html")

@app.get("/billing.html")
def serve_billing():
    """Serve billing page"""
    return FileResponse("static/billing.html")

@app.get("/reports.html")
def serve_reports():
    """Serve reports page"""
    return FileResponse("static/reports.html")

@app.get("/products.html")
def serve_products():
    """Serve products management page"""
    return FileResponse("static/products.html")

# ==================== Health Check ====================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Grocery Management System is running"}

# Note: For local development, run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
# For production: uvicorn main:app --host 0.0.0.0 --port 8000
