from app_init import mysql,app

def create_tables():
    # Establish a connection to MySQL
    with app.app_context():
        conn = mysql.connect
        cursor = conn.cursor()
        queries = [
            """
            CREATE TABLE IF NOT EXISTS signup (
                id INT AUTO_INCREMENT PRIMARY KEY,       -- Auto-incremented ID
                username VARCHAR(50) NOT NULL,            -- Username field (max length 50)
                password VARCHAR(20) NOT NULL             -- Password field (max length 20)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS product (
                product_name VARCHAR(80) NOT NULL,       -- Product name (max length 80)
                productPrice INT NOT NULL,               -- Product price (integer)
                productSize INT NOT NULL,                -- Product size (integer)
                ProductID INT NOT NULL,                  -- Product ID (integer)
                PRIMARY KEY (ProductID)                  -- Set ProductID as the primary key
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,        -- Auto-incremented ID
                buyer_contact VARCHAR(15) NOT NULL,        -- Contact number
                buyer_email VARCHAR(255) NOT NULL,         -- Email address
                product_name VARCHAR(255) NOT NULL,        -- Product name
                product_price DECIMAL(10,2) NOT NULL,      -- Price
                product_quantity INT NOT NULL,             -- Quantity
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Default timestamp for order date
            )
            """
        ]

        try:
            # Execute each query
            for query in queries:
                cursor.execute(query)
            conn.commit()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            conn.close()
if __name__ == "__main__":
    create_tables()
