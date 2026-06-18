"""
Initialize sample database with demo data
"""
import sqlite3
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def init_sqlite_db(db_path: str = "./analytics.db"):
    """Initialize SQLite database with sample data"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create tables
        logger.info("Creating tables...")
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                segment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                product_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                revenue REAL NOT NULL,
                segment TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """)
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] > 0:
            logger.info("Database already initialized with data")
            conn.close()
            return
        
        # Insert sample products
        logger.info("Inserting sample products...")
        products = [
            ("Laptop Pro", "Electronics", 1299),
            ("Wireless Mouse", "Accessories", 29),
            ("Monitor 4K", "Electronics", 599),
            ("Desk Chair", "Furniture", 299),
            ("USB Cable", "Accessories", 9),
            ("Standing Desk", "Furniture", 599),
            ("Keyboard Mechanical", "Accessories", 149),
            ("Webcam HD", "Electronics", 79),
        ]
        cursor.executemany(
            "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
            products
        )
        
        # Insert sample customers
        logger.info("Inserting sample customers...")
        customers = [
            ("john@company.com", "John Smith", "Enterprise"),
            ("jane@startup.com", "Jane Doe", "SMB"),
            ("bob@corp.com", "Bob Johnson", "Enterprise"),
            ("alice@business.com", "Alice Williams", "SMB"),
            ("charlie@enterprise.com", "Charlie Brown", "Enterprise"),
            ("diana@small.com", "Diana Prince", "SMB"),
        ]
        cursor.executemany(
            "INSERT INTO customers (email, name, segment) VALUES (?, ?, ?)",
            customers
        )
        
        # Insert sample sales data
        logger.info("Inserting sample sales data...")
        base_date = datetime.now() - timedelta(days=30)
        
        sales_data = []
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            # Generate 2-4 sales per day
            for _ in range(random.randint(2, 4)):
                product_id = random.randint(1, 8)
                customer_id = random.randint(1, 6)
                quantity = random.randint(1, 20)
                
                # Get product price
                cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
                price = cursor.fetchone()[0]
                revenue = price * quantity
                
                # Get customer segment
                cursor.execute("SELECT segment FROM customers WHERE id = ?", (customer_id,))
                segment = cursor.fetchone()[0]
                
                sales_data.append((
                    current_date.date(),
                    product_id,
                    customer_id,
                    quantity,
                    revenue,
                    segment
                ))
        
        cursor.executemany(
            """INSERT INTO sales (date, product_id, customer_id, quantity, revenue, segment)
               VALUES (?, ?, ?, ?, ?, ?)""",
            sales_data
        )
        
        # Create indexes
        logger.info("Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales(product_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_customer_id ON sales(customer_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)")
        
        conn.commit()
        logger.info("Database initialization complete!")
        
        # Show statistics
        cursor.execute("SELECT COUNT(*) FROM products")
        print(f"✓ Products: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM customers")
        print(f"✓ Customers: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM sales")
        print(f"✓ Sales: {cursor.fetchone()[0]}")
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    import logging.config
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    init_sqlite_db()
