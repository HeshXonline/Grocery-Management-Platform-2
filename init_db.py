from config import Base, engine
from models import Product, Sale, SaleItem

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("\nTables created:")
    print("- products")
    print("- sales")
    print("- sale_items")

if __name__ == "__main__":
    init_database()
