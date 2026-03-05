"""
Generate sample e-commerce data for the AI analytics demo.
This script creates realistic data for customers, products, orders, reviews, and inventory.
"""

import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

# Sample data
CATEGORIES = [
    ("Electronics", "Electronic devices and accessories"),
    ("Clothing", "Fashion and apparel"),
    ("Home & Garden", "Home improvement and garden supplies"),
    ("Books", "Books and educational materials"),
    ("Sports & Outdoors", "Sports equipment and outdoor gear"),
    ("Toys & Games", "Toys, games, and entertainment"),
    ("Beauty & Health", "Beauty products and health supplements"),
    ("Food & Beverages", "Gourmet food and beverages"),
]

PRODUCTS = {
    "Electronics": [
        ("Wireless Headphones", "High-quality Bluetooth headphones", 79.99, 35.00),
        ("Smart Watch", "Fitness tracking smartwatch", 199.99, 90.00),
        ("Laptop Stand", "Ergonomic aluminum laptop stand", 49.99, 20.00),
        ("USB-C Hub", "7-in-1 USB-C multiport adapter", 39.99, 15.00),
        ("Wireless Mouse", "Ergonomic wireless mouse", 29.99, 12.00),
        ("Mechanical Keyboard", "RGB mechanical gaming keyboard", 129.99, 55.00),
        ("Webcam HD", "1080p HD webcam with microphone", 69.99, 30.00),
        ("Phone Case", "Protective phone case", 19.99, 5.00),
        ("Screen Protector", "Tempered glass screen protector", 14.99, 3.00),
        ("Charging Cable", "Fast charging USB cable", 12.99, 4.00),
    ],
    "Clothing": [
        ("Cotton T-Shirt", "Comfortable cotton t-shirt", 24.99, 8.00),
        ("Denim Jeans", "Classic fit denim jeans", 59.99, 25.00),
        ("Running Shoes", "Lightweight running shoes", 89.99, 40.00),
        ("Winter Jacket", "Warm winter jacket", 149.99, 65.00),
        ("Casual Sneakers", "Everyday casual sneakers", 69.99, 30.00),
        ("Hoodie", "Comfortable pullover hoodie", 44.99, 18.00),
        ("Dress Shirt", "Formal dress shirt", 39.99, 15.00),
        ("Yoga Pants", "Stretchy yoga pants", 34.99, 12.00),
        ("Baseball Cap", "Adjustable baseball cap", 19.99, 6.00),
        ("Socks Pack", "Pack of 6 athletic socks", 14.99, 5.00),
    ],
    "Home & Garden": [
        ("LED Desk Lamp", "Adjustable LED desk lamp", 34.99, 15.00),
        ("Storage Bins", "Set of 3 storage bins", 29.99, 10.00),
        ("Garden Tools Set", "5-piece garden tool set", 44.99, 18.00),
        ("Throw Pillows", "Decorative throw pillows (2-pack)", 24.99, 8.00),
        ("Wall Clock", "Modern wall clock", 39.99, 15.00),
        ("Plant Pot", "Ceramic plant pot with drainage", 19.99, 6.00),
        ("Picture Frame", "Wooden picture frame", 16.99, 5.00),
        ("Candle Set", "Scented candle set (3-pack)", 27.99, 10.00),
        ("Door Mat", "Welcome door mat", 22.99, 8.00),
        ("Curtains", "Blackout curtains", 49.99, 20.00),
    ],
    "Books": [
        ("Python Programming", "Learn Python programming", 39.99, 12.00),
        ("Business Strategy", "Modern business strategy guide", 29.99, 10.00),
        ("Cookbook", "Healthy cooking recipes", 24.99, 8.00),
        ("Mystery Novel", "Bestselling mystery thriller", 14.99, 5.00),
        ("Self-Help Book", "Personal development guide", 19.99, 6.00),
        ("History Book", "World history overview", 34.99, 12.00),
        ("Science Fiction", "Sci-fi adventure novel", 16.99, 5.00),
        ("Biography", "Inspiring biography", 22.99, 8.00),
        ("Art Book", "Modern art collection", 44.99, 15.00),
        ("Children's Book", "Illustrated children's story", 12.99, 4.00),
    ],
    "Sports & Outdoors": [
        ("Yoga Mat", "Non-slip yoga mat", 29.99, 12.00),
        ("Dumbbell Set", "Adjustable dumbbell set", 89.99, 40.00),
        ("Water Bottle", "Insulated water bottle", 24.99, 8.00),
        ("Camping Tent", "4-person camping tent", 149.99, 65.00),
        ("Hiking Backpack", "40L hiking backpack", 79.99, 35.00),
        ("Resistance Bands", "Set of 5 resistance bands", 19.99, 6.00),
        ("Jump Rope", "Speed jump rope", 14.99, 5.00),
        ("Sleeping Bag", "3-season sleeping bag", 59.99, 25.00),
        ("Bike Helmet", "Safety bike helmet", 44.99, 18.00),
        ("Sports Gloves", "Training gloves", 24.99, 8.00),
    ],
    "Toys & Games": [
        ("Board Game", "Family board game", 34.99, 12.00),
        ("Puzzle 1000pc", "1000-piece jigsaw puzzle", 19.99, 6.00),
        ("Building Blocks", "Creative building blocks set", 44.99, 18.00),
        ("Action Figure", "Collectible action figure", 24.99, 8.00),
        ("Stuffed Animal", "Plush stuffed animal", 16.99, 5.00),
        ("Card Game", "Strategy card game", 14.99, 5.00),
        ("Remote Control Car", "RC racing car", 49.99, 20.00),
        ("Art Supplies", "Kids art supplies set", 29.99, 10.00),
        ("Educational Toy", "STEM learning toy", 39.99, 15.00),
        ("Outdoor Play Set", "Outdoor sports set", 34.99, 12.00),
    ],
    "Beauty & Health": [
        ("Face Moisturizer", "Hydrating face moisturizer", 29.99, 10.00),
        ("Shampoo & Conditioner", "Natural hair care set", 24.99, 8.00),
        ("Vitamin Supplements", "Daily multivitamin", 19.99, 6.00),
        ("Essential Oils", "Aromatherapy essential oils set", 34.99, 12.00),
        ("Facial Cleanser", "Gentle facial cleanser", 16.99, 5.00),
        ("Body Lotion", "Moisturizing body lotion", 14.99, 5.00),
        ("Makeup Brush Set", "Professional makeup brushes", 39.99, 15.00),
        ("Nail Care Kit", "Complete nail care kit", 22.99, 8.00),
        ("Hair Dryer", "Professional hair dryer", 59.99, 25.00),
        ("Massage Oil", "Relaxing massage oil", 19.99, 6.00),
    ],
    "Food & Beverages": [
        ("Organic Coffee", "Premium organic coffee beans", 24.99, 8.00),
        ("Green Tea", "Organic green tea (50 bags)", 14.99, 5.00),
        ("Protein Powder", "Whey protein powder", 44.99, 18.00),
        ("Olive Oil", "Extra virgin olive oil", 19.99, 6.00),
        ("Honey", "Raw organic honey", 16.99, 5.00),
        ("Dark Chocolate", "Premium dark chocolate bar", 9.99, 3.00),
        ("Nuts Mix", "Mixed nuts (1lb)", 12.99, 4.00),
        ("Pasta Set", "Gourmet pasta variety pack", 22.99, 8.00),
        ("Spice Set", "International spice collection", 29.99, 10.00),
        ("Energy Bars", "Protein energy bars (12-pack)", 19.99, 6.00),
    ],
}

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
               "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
               "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White"]

COUNTRIES = ["USA", "Canada", "UK", "Germany", "France", "Australia", "Japan", "Spain", "Italy", "Netherlands"]

CITIES = {
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "UK": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Yokohama", "Nagoya"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    "Italy": ["Rome", "Milan", "Naples", "Turin", "Florence"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
}

ORDER_STATUSES = ["delivered", "delivered", "delivered", "delivered", "shipped", "processing", "cancelled"]

REVIEW_COMMENTS = {
    5: ["Excellent product!", "Love it!", "Highly recommend!", "Perfect!", "Amazing quality!"],
    4: ["Very good", "Happy with purchase", "Good value", "Satisfied", "Nice product"],
    3: ["It's okay", "Average", "Meets expectations", "Decent", "Fair"],
    2: ["Not great", "Disappointed", "Could be better", "Below expectations", "Mediocre"],
    1: ["Poor quality", "Waste of money", "Do not buy", "Terrible", "Very disappointed"],
}


def create_database(db_path: str):
    """Create the database and tables."""
    schema_path = Path(__file__).parent.parent.parent / "database" / "schema.sql"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    conn.commit()
    return conn


def seed_categories(cursor):
    """Insert categories."""
    print("Seeding categories...")
    category_ids = {}
    for i, (name, description) in enumerate(CATEGORIES):
        cursor.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (name, description)
        )
        category_ids[name] = cursor.lastrowid
    return category_ids


def seed_products(cursor, category_ids):
    """Insert products."""
    print("Seeding products...")
    products = []
    product_id = 1
    
    for category, items in PRODUCTS.items():
        category_id = category_ids[category]
        for name, desc, price, cost in items:
            sku = f"SKU-{product_id:05d}"
            products.append((category_id, name, desc, price, cost, sku))
            product_id += 1
    
    cursor.executemany(
        "INSERT INTO products (category_id, name, description, price, cost, sku) VALUES (?, ?, ?, ?, ?, ?)",
        products
    )
    return product_id - 1


def seed_customers(cursor, num_customers=200):
    """Insert customers."""
    print(f"Seeding {num_customers} customers...")
    customers = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    for i in range(num_customers):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{i}@email.com"
        country = random.choice(COUNTRIES)
        city = random.choice(CITIES[country])
        reg_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        customers.append((name, email, country, city, reg_date.date()))
    
    cursor.executemany(
        "INSERT INTO customers (name, email, country, city, registration_date) VALUES (?, ?, ?, ?, ?)",
        customers
    )
    return num_customers


def seed_orders_and_items(cursor, num_customers, num_products, num_orders=500):
    """Insert orders and order items."""
    print(f"Seeding {num_orders} orders with items...")
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 2, 28)
    
    for _ in range(num_orders):
        customer_id = random.randint(1, num_customers)
        order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        status = random.choice(ORDER_STATUSES)
        
        # Create order
        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_cost, tax_amount) VALUES (?, ?, ?, ?, ?, ?)",
            (customer_id, order_date.date(), status, 0, 0, 0)  # Will update total
        )
        order_id = cursor.lastrowid
        
        # Add 1-5 items to order
        num_items = random.randint(1, 5)
        order_total = 0
        
        for _ in range(num_items):
            product_id = random.randint(1, num_products)
            
            # Get product price
            cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
            price = cursor.fetchone()[0]
            
            quantity = random.randint(1, 3)
            discount = random.choice([0, 0, 0, 0, 5, 10])  # Mostly no discount
            subtotal = (price * quantity) * (1 - discount / 100)
            order_total += subtotal
            
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal, discount) VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, product_id, quantity, price, subtotal, discount)
            )
        
        # Update order total
        shipping = 5.99 if order_total < 50 else 0
        tax = order_total * 0.08
        total = order_total + shipping + tax
        
        cursor.execute(
            "UPDATE orders SET total_amount = ?, shipping_cost = ?, tax_amount = ? WHERE id = ?",
            (total, shipping, tax, order_id)
        )


def seed_reviews(cursor, num_products, num_customers):
    """Insert product reviews."""
    print("Seeding reviews...")
    
    # Generate reviews for about 60% of products
    num_reviews = int(num_products * 0.6 * 3)  # Average 3 reviews per reviewed product
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 2, 28)
    
    for _ in range(num_reviews):
        product_id = random.randint(1, num_products)
        customer_id = random.randint(1, num_customers)
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]  # Skewed positive
        comment = random.choice(REVIEW_COMMENTS[rating])
        review_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        helpful_count = random.randint(0, 50)
        
        try:
            cursor.execute(
                "INSERT INTO reviews (product_id, customer_id, rating, comment, review_date, helpful_count) VALUES (?, ?, ?, ?, ?, ?)",
                (product_id, customer_id, rating, comment, review_date.date(), helpful_count)
            )
        except sqlite3.IntegrityError:
            # Skip if customer already reviewed this product
            pass


def seed_inventory(cursor, num_products):
    """Insert inventory data."""
    print("Seeding inventory...")
    
    warehouses = ["Warehouse A", "Warehouse B", "Warehouse C"]
    
    for product_id in range(1, num_products + 1):
        quantity = random.randint(0, 500)
        warehouse = random.choice(warehouses)
        reorder_level = random.randint(10, 50)
        
        cursor.execute(
            "INSERT INTO inventory (product_id, quantity, warehouse, reorder_level) VALUES (?, ?, ?, ?)",
            (product_id, quantity, warehouse, reorder_level)
        )


def update_customer_lifetime_values(cursor):
    """Update customer lifetime values based on orders."""
    print("Updating customer lifetime values...")
    cursor.execute("""
        UPDATE customers
        SET lifetime_value = (
            SELECT COALESCE(SUM(total_amount), 0)
            FROM orders
            WHERE orders.customer_id = customers.id
        )
    """)


def main():
    """Main function to seed the database."""
    db_path = Path(__file__).parent.parent.parent / "database" / "ecommerce.db"
    
    # Remove existing database if it exists
    if db_path.exists():
        print(f"Removing existing database at: {db_path}")
        db_path.unlink()
    
    print(f"Creating database at: {db_path}")
    conn = create_database(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Seed data
        category_ids = seed_categories(cursor)
        num_products = seed_products(cursor, category_ids)
        num_customers = seed_customers(cursor, num_customers=200)
        seed_orders_and_items(cursor, num_customers, num_products, num_orders=500)
        seed_reviews(cursor, num_products, num_customers)
        seed_inventory(cursor, num_products)
        update_customer_lifetime_values(cursor)
        
        conn.commit()
        print("\n✅ Database seeded successfully!")
        
        # Print statistics
        cursor.execute("SELECT COUNT(*) FROM customers")
        print(f"   Customers: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        print(f"   Products: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        print(f"   Orders: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM order_items")
        print(f"   Order Items: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM reviews")
        print(f"   Reviews: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT SUM(total_amount) FROM orders WHERE status = 'delivered'")
        total_revenue = cursor.fetchone()[0]
        print(f"   Total Revenue (delivered): ${total_revenue:,.2f}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

# Made with Bob
