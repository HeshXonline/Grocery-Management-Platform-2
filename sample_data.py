from config import SessionLocal
from models import Product

def add_sample_products():
    """Add sample products to the database"""
    db = SessionLocal()
    
    sample_products = [
        # Rice & Grains
        {"name": "Basmati Rice", "category": "Rice & Grains", "buying_price": 80, "selling_price": 100, "stock_quantity": 50},
        {"name": "Ponni Rice", "category": "Rice & Grains", "buying_price": 50, "selling_price": 65, "stock_quantity": 60},
        {"name": "Wheat Flour", "category": "Rice & Grains", "buying_price": 35, "selling_price": 45, "stock_quantity": 40},
        {"name": "Rice Flour", "category": "Rice & Grains", "buying_price": 30, "selling_price": 40, "stock_quantity": 30},
        
        # Pulses & Lentils
        {"name": "Toor Dal", "category": "Pulses & Lentils", "buying_price": 100, "selling_price": 120, "stock_quantity": 35},
        {"name": "Moong Dal", "category": "Pulses & Lentils", "buying_price": 90, "selling_price": 110, "stock_quantity": 30},
        {"name": "Chana Dal", "category": "Pulses & Lentils", "buying_price": 70, "selling_price": 85, "stock_quantity": 25},
        {"name": "Urad Dal", "category": "Pulses & Lentils", "buying_price": 95, "selling_price": 115, "stock_quantity": 28},
        
        # Spices
        {"name": "Turmeric Powder", "category": "Spices", "buying_price": 120, "selling_price": 150, "stock_quantity": 20},
        {"name": "Chilli Powder", "category": "Spices", "buying_price": 150, "selling_price": 180, "stock_quantity": 18},
        {"name": "Coriander Powder", "category": "Spices", "buying_price": 80, "selling_price": 100, "stock_quantity": 22},
        {"name": "Garam Masala", "category": "Spices", "buying_price": 200, "selling_price": 250, "stock_quantity": 15},
        {"name": "Cumin Seeds", "category": "Spices", "buying_price": 300, "selling_price": 350, "stock_quantity": 12},
        
        # Cooking Oils
        {"name": "Sunflower Oil (1L)", "category": "Cooking Oils", "buying_price": 140, "selling_price": 170, "stock_quantity": 40},
        {"name": "Groundnut Oil (1L)", "category": "Cooking Oils", "buying_price": 180, "selling_price": 220, "stock_quantity": 30},
        {"name": "Coconut Oil (500ml)", "category": "Cooking Oils", "buying_price": 100, "selling_price": 130, "stock_quantity": 25},
        
        # Sugar & Salt
        {"name": "Sugar", "category": "Sugar & Salt", "buying_price": 38, "selling_price": 50, "stock_quantity": 80},
        {"name": "Rock Salt", "category": "Sugar & Salt", "buying_price": 15, "selling_price": 20, "stock_quantity": 60},
        {"name": "Jaggery", "category": "Sugar & Salt", "buying_price": 60, "selling_price": 80, "stock_quantity": 35},
        
        # Beverages
        {"name": "Tea Powder (250g)", "category": "Beverages", "buying_price": 120, "selling_price": 150, "stock_quantity": 45},
        {"name": "Coffee Powder (200g)", "category": "Beverages", "buying_price": 180, "selling_price": 220, "stock_quantity": 30},
        
        # Snacks & Biscuits
        {"name": "Parle-G Biscuits", "category": "Snacks & Biscuits", "buying_price": 10, "selling_price": 12, "stock_quantity": 100},
        {"name": "Good Day Cookies", "category": "Snacks & Biscuits", "buying_price": 25, "selling_price": 30, "stock_quantity": 60},
        {"name": "Mixture (500g)", "category": "Snacks & Biscuits", "buying_price": 80, "selling_price": 100, "stock_quantity": 40},
        
        # Personal Care
        {"name": "Bath Soap", "category": "Personal Care", "buying_price": 25, "selling_price": 35, "stock_quantity": 70},
        {"name": "Shampoo Sachet", "category": "Personal Care", "buying_price": 5, "selling_price": 7, "stock_quantity": 150},
        {"name": "Toothpaste", "category": "Personal Care", "buying_price": 45, "selling_price": 60, "stock_quantity": 50},
        
        # Cleaning Supplies
        {"name": "Detergent Powder (1kg)", "category": "Cleaning Supplies", "buying_price": 120, "selling_price": 150, "stock_quantity": 35},
        {"name": "Dishwash Bar", "category": "Cleaning Supplies", "buying_price": 15, "selling_price": 20, "stock_quantity": 60},
        
        # Dairy Products
        {"name": "Milk (500ml)", "category": "Dairy Products", "buying_price": 25, "selling_price": 30, "stock_quantity": 40},
        {"name": "Curd (500g)", "category": "Dairy Products", "buying_price": 30, "selling_price": 40, "stock_quantity": 25},
        
        # Instant Foods
        {"name": "Maggi Noodles", "category": "Instant Foods", "buying_price": 12, "selling_price": 15, "stock_quantity": 80},
        {"name": "Poha (500g)", "category": "Instant Foods", "buying_price": 35, "selling_price": 45, "stock_quantity": 40},
        
        # Vegetables (Sample - Update daily)
        {"name": "Onion (per kg)", "category": "Vegetables", "buying_price": 30, "selling_price": 40, "stock_quantity": 50},
        {"name": "Potato (per kg)", "category": "Vegetables", "buying_price": 25, "selling_price": 35, "stock_quantity": 60},
        {"name": "Tomato (per kg)", "category": "Vegetables", "buying_price": 35, "selling_price": 45, "stock_quantity": 40},
    ]
    
    try:
        # Check if products already exist
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} products.")
            response = input("Do you want to add more sample products? (yes/no): ")
            if response.lower() != 'yes':
                print("Skipping sample data creation.")
                db.close()
                return
        
        print(f"Adding {len(sample_products)} sample products...")
        
        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print(f"✓ Successfully added {len(sample_products)} sample products!")
        
        # Display summary
        print("\nProduct Summary by Category:")
        categories = {}
        for product in sample_products:
            cat = product["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"  - {category}: {count} products")
        
    except Exception as e:
        db.rollback()
        print(f"Error adding sample products: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_products()
