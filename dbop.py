
# get_total_products()

# get_total_sales()

# get_total_profit()

# get_low_stock_count()

# get_all_products()

# search_product()

# execute_query()

import sqlite3

def get_connection():
    conn = sqlite3.connect("Supermarket.db")
    return conn

conn = get_connection()
cursor = conn.cursor()


cursor.execute("SELECT SUM(selling_price_at_sale) from sales")
ts_result = cursor.fetchone()[0]


cursor.execute("SELECT COUNT(product_id) from products ")
tp_result = cursor.fetchone()[0]

cursor.execute("SELECT SUM((selling_price_at_sale - cost_price_at_sale) * quantity) FROM sales")
p_result = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM products WHERE stock_quantity < 60")
ls_result = cursor.fetchone()[0]

def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name,
               stock_quantity,
               cost_price,
               selling_price
        FROM products
    """)

    products = cursor.fetchall()

    conn.close()
    return products

def search_products(product_name):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT product_name,
                   stock_quantity,
                   cost_price,
                   selling_price
            FROM products 
            where product_name like ?
            """,    ('%' + product_name + '%', ))

    products = cursor.fetchall()
    
    conn.close()
    return products


def get_table_product():
    conn =get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PRODUCTS')

    prod = cursor.fetchall()

    conn.close()
    return prod

# def get_table_sales():
#     conn =get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM sales')

#     sales = cursor.fetchall()

#     conn.close()
#     return sales



# DB_NAME = "Supermarket.db"   # Change if your database name is different


def get_database_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema = ""

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        if table_name == "sqlite_sequence":
            continue

        schema += f"\nTable: {table_name}\n"

        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        for col in columns:
            schema += f"- {col[1]} ({col[2]})\n"

    conn.close()

    return schema

def execute_sql_query(sql_query, db_path):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(sql_query)

    result = cursor.fetchall()

    conn.close()

    return result