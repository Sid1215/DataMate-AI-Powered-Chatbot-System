import sqlite3

conn = sqlite3.connect("Supermarket.db")

cursor = conn.cursor()

# Creating product table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    stock_quantity INTEGER,
    cost_price REAL,
    selling_price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Creating sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    cost_price_at_sale REAL,
    selling_price_at_sale REAL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")




# INSERT PRODUCTS (100 rows)

products = [
    ("Laptop", "Electronics", "Computers", 50, 50000, 48000),
    ("Smartphone", "Electronics", "Mobile Phones", 80, 20000, 19000),
    ("Tablet", "Electronics", "Mobile Devices", 60, 15000, 14000),
    ("Headphones", "Electronics", "Audio", 120, 1500, 1400),
    ("Speaker", "Electronics", "Audio", 90, 2000, 1800),
    ("Camera", "Electronics", "Photography", 30, 45000, 43000),
    ("Printer", "Electronics", "Office Equipment", 40, 7000, 6500),
    ("Router", "Electronics", "Networking", 70, 2500, 2300),
    ("Keyboard", "Electronics", "Accessories", 150, 800, 750),
    ("Mouse", "Electronics", "Accessories", 180, 500, 450),
    ("TV", "Electronics", "Entertainment", 25, 40000, 38000),
    ("Microwave", "Electronics", "Appliances", 35, 8000, 7500),
    ("Refrigerator", "Electronics", "Appliances", 20, 30000, 28000),
    ("Washing Machine", "Electronics", "Appliances", 15, 25000, 24000),
    ("Power Bank", "Electronics", "Mobile Accessories", 110, 1200, 1100),

    ("Watch", "Fashion", "Wrist Watches", 100, 2000, 2500),
    ("Shoes", "Fashion", "Footwear", 150, 1200, 1800),
    ("T-Shirt", "Fashion", "Clothing", 200, 300, 600),
    ("Jeans", "Fashion", "Clothing", 120, 800, 1500),
    ("Jacket", "Fashion", "Outerwear", 90, 1500, 3000),
    ("Cap", "Fashion", "Accessories", 130, 200, 500),
    ("Socks", "Fashion", "Accessories", 180, 50, 120),
    ("Belt", "Fashion", "Accessories", 140, 300, 800),

    ("Rice Bag", "Grocery", "Staples", 300, 800, 950),
    ("Wheat Flour", "Grocery", "Staples", 280, 500, 650),
    ("Sugar", "Grocery", "Staples", 220, 400, 550),
    ("Salt", "Grocery", "Essentials", 300, 100, 150),
    ("Cooking Oil", "Grocery", "Essentials", 200, 1200, 1500),
    ("Spices Pack", "Grocery", "Masala", 180, 200, 350),
    ("Tea Powder", "Grocery", "Beverage Essentials", 160, 250, 450),
    ("Coffee Powder", "Grocery", "Beverage Essentials", 140, 300, 550),

    ("Milk Pack", "Dairy", "Milk", 200, 40, 60),
    ("Butter", "Dairy", "Dairy Products", 120, 200, 300),
    ("Cheese", "Dairy", "Dairy Products", 100, 300, 450),
    ("Yogurt", "Dairy", "Dairy Products", 150, 50, 80),
    ("Paneer", "Dairy", "Dairy Products", 130, 250, 400),

    ("Egg Tray", "Poultry", "Eggs", 200, 120, 180),
    ("Chicken", "Poultry", "Meat", 150, 200, 300),

    ("Apple", "Fruits", "Fresh Fruits", 250, 120, 180),
    ("Banana", "Fruits", "Fresh Fruits", 300, 40, 70),
    ("Orange", "Fruits", "Fresh Fruits", 220, 60, 100),
    ("Mango", "Fruits", "Seasonal Fruits", 180, 80, 150),
    ("Grapes", "Fruits", "Fresh Fruits", 200, 90, 140),

    ("Potato", "Vegetables", "Root Vegetables", 350, 20, 40),
    ("Onion", "Vegetables", "Root Vegetables", 300, 25, 50),
    ("Tomato", "Vegetables", "Fresh Vegetables", 280, 30, 60),
    ("Carrot", "Vegetables", "Root Vegetables", 200, 35, 70),
    ("Cabbage", "Vegetables", "Leafy Vegetables", 180, 25, 60),

    ("Soap", "Personal Care", "Hygiene", 250, 25, 50),
    ("Shampoo", "Personal Care", "Hair Care", 150, 120, 220),
    ("Toothpaste", "Personal Care", "Oral Care", 180, 60, 120),
    ("Face Wash", "Personal Care", "Skin Care", 140, 150, 300),
    ("Body Lotion", "Personal Care", "Skin Care", 130, 200, 400),

    ("Notebook", "Stationery", "Office Supplies", 200, 50, 120),
    ("Pen Pack", "Stationery", "Office Supplies", 250, 40, 100),
    ("Marker", "Stationery", "Office Supplies", 150, 30, 90),
    ("Stapler", "Stationery", "Office Supplies", 120, 80, 200),

    ("Water Bottle", "Home", "Kitchen Items", 150, 100, 250),
    ("Lunch Box", "Home", "Kitchen Items", 130, 150, 350),
    ("Plate Set", "Home", "Kitchen Items", 100, 500, 900),
    ("Glass Set", "Home", "Kitchen Items", 110, 300, 700),

    ("Detergent Powder", "Cleaning", "Laundry", 220, 200, 350),
    ("Dishwash Liquid", "Cleaning", "Kitchen Cleaning", 180, 120, 250),
    ("Floor Cleaner", "Cleaning", "Home Cleaning", 160, 150, 300),
    ("Toilet Cleaner", "Cleaning", "Bathroom Cleaning", 140, 130, 280),

    ("Cereal Box", "Food", "Breakfast", 160, 200, 350),
    ("Oats Pack", "Food", "Breakfast", 150, 180, 320),
    ("Biscuits", "Food", "Snacks", 300, 20, 50),
    ("Chips Pack", "Food", "Snacks", 280, 15, 40),
    ("Chocolate", "Food", "Snacks", 200, 50, 120),

    ("Cold Drink", "Beverages", "Soft Drinks", 260, 30, 70),
    ("Juice Pack", "Beverages", "Juices", 200, 40, 90),
    ("Energy Drink", "Beverages", "Energy Drinks", 180, 80, 150),
    ("Mineral Water", "Beverages", "Water", 300, 10, 25),

    ("Bag", "Accessories", "Travel", 120, 800, 1500),
    ("Wallet", "Accessories", "Fashion", 140, 400, 900),
    ("Sunglasses", "Accessories", "Fashion", 100, 500, 1200),
    ("Umbrella", "Accessories", "Utility", 110, 200, 500),
    ("Helmet", "Accessories", "Safety", 90, 1000, 2000),
    ("Torch", "Utility", "Lighting", 130, 150, 400),
    ("Extension Board", "Utility", "Electrical", 120, 300, 700),
    ("Gas Stove", "Home Appliances", "Kitchen", 80, 2500, 4000),
    ("Mixer Grinder", "Home Appliances", "Kitchen", 70, 3000, 5000),
    ("Iron Box", "Home Appliances", "Utility", 90, 1200, 2500),
]

cursor.executemany("""
INSERT INTO products (
    product_name, category, sub_category, stock_quantity,
    cost_price, selling_price
) VALUES (?, ?, ?, ?, ?, ?)
""", products)

# INSERT SALES (100 rows)

sales = [
    (1, 2, 50000, 48000),
    (2, 1, 20000, 19500),
    (3, 3, 15000, 14500),
    (4, 5, 1500, 1400),
    (5, 2, 2000, 1850),
    (6, 1, 45000, 43000),
    (7, 2, 7000, 6600),
    (8, 3, 2500, 2300),
    (9, 4, 800, 750),
    (10, 6, 500, 450),

    (11, 1, 40000, 38500),
    (12, 2, 8000, 7600),
    (13, 1, 30000, 28500),
    (14, 1, 25000, 24000),
    (15, 3, 1200, 1100),

    # Profit products
    (16, 4, 2000, 2600),
    (17, 6, 1200, 1800),
    (18, 8, 300, 600),
    (19, 5, 800, 1500),
    (20, 3, 1500, 3000),

    (21, 7, 200, 500),
    (22, 10, 50, 120),
    (23, 5, 300, 800),

    (24, 20, 800, 950),
    (25, 18, 500, 650),
    (26, 15, 400, 550),
    (27, 25, 100, 150),
    (28, 10, 1200, 1500),

    (29, 12, 200, 350),
    (30, 8, 250, 450),
    (31, 6, 300, 550),

    (32, 25, 40, 60),
    (33, 15, 200, 300),
    (34, 10, 300, 450),
    (35, 20, 50, 80),
    (36, 12, 250, 400),

    (37, 30, 120, 180),
    (38, 20, 200, 300),

    (39, 50, 120, 180),
    (40, 60, 40, 70),
    (41, 30, 60, 100),
    (42, 20, 80, 150),
    (43, 25, 90, 140),

    (44, 100, 20, 40),
    (45, 80, 25, 50),
    (46, 60, 30, 60),
    (47, 40, 35, 70),
    (48, 30, 25, 60),

    (49, 70, 25, 50),
    (50, 50, 120, 220),
    (51, 40, 60, 120),
    (52, 35, 150, 300),
    (53, 20, 200, 400),

    (54, 60, 50, 120),
    (55, 70, 40, 100),
    (56, 80, 30, 90),
    (57, 20, 80, 200),

    (58, 50, 100, 250),
    (59, 40, 150, 350),
    (60, 30, 500, 900),
    (61, 35, 300, 700),

    (62, 60, 200, 350),
    (63, 50, 120, 250),
    (64, 40, 150, 300),
    (65, 30, 130, 280),

    (66, 45, 200, 350),
    (67, 40, 180, 320),
    (68, 60, 20, 50),
    (69, 70, 15, 40),
    (70, 50, 50, 120),

    (71, 90, 30, 70),
    (72, 60, 40, 90),
    (73, 50, 80, 150),
    (74, 100, 10, 25),

    (75, 40, 800, 1500),
    (76, 35, 400, 900),
    (77, 30, 500, 1200),
    (78, 25, 200, 500),

    (79, 20, 1000, 2000),
    (80, 30, 150, 400),
    (81, 40, 300, 700),

    (82, 25, 2500, 4000),
    (83, 20, 3000, 5000),
    (84, 30, 1200, 2500),
]

cursor.executemany("""
INSERT INTO sales (
    product_id, quantity,
    cost_price_at_sale, selling_price_at_sale
) VALUES (?, ?, ?, ?)
""", sales)

# COMMIT & CLOSE

conn.commit()
conn.close()

print("✅ 100 Products and 100 Sales inserted successfully!")