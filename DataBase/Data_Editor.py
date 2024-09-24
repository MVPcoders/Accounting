import sqlite3



class DataBase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()


    def execute_query(self, query,params=None):
        if params is None:
            params = []

        self.cursor.execute(query,params)
        self.conn.commit()


    def fetch_one_query(self, query, params=None):
        if params is None:
            params = []

        self.cursor.execute(query, params)
        current_row = self.cursor.fetchone()
        self.conn.commit()
        return current_row


    def fetch_all_query(self, query, params=None):
        if params is None:
            params = []

        self.cursor.execute(query, params)
        all_rows = self.cursor.fetchall()
        self.conn.commit()
        return all_rows


    def close_query(self):
        self.conn.close()





class Products(DataBase):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.create_table()


    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS product_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                brand TEXT NOT NULL,
                buy_price  TEXT NOT NULL,
                sell_price TEXT NOT NULL,
                unit TEXT NOT NULL,
                inventory FLOAT NOT NULL
                );
                """
        self.execute_query(query,params=None)


    def add_product(self, product, brand, buy_price, sell_price, unit, inventory):
        query = "INSERT INTO product_table (product, brand,  buy_price,  sell_price, unit, inventory) VALUES (?, ?, ?, ?, ?, ?);"
        self.execute_query(query, (product, brand, buy_price, sell_price, unit, inventory))


    def update_product(self,  id, product, brand, buy_price, sell_price, unit, inventory):
        query = "UPDATE product_table SET product=? , brand=?, buy_price=?, sell_price=?, unit=?, inventory=?  WHERE id=?"
        self.execute_query(query, (product, brand, buy_price, sell_price, unit, inventory, id))


    def delete_product(self, id):
        query = "DELETE FROM product_table WHERE id=?"
        self.execute_query(query, (id,))


    def get_all_products(self):
        query = "SELECT * FROM product_table"
        all_products = self.fetch_all_query(query)
        return all_products


    def get_product_by_id(self, id):
        query = "SELECT * FROM product_table WHERE id=?"
        product = self.fetch_one_query(query, (id,))
        return product


    def get_product_by_name(self, name):
        query = "SELECT * FROM product_table WHERE product=?"
        product = self.fetch_one_query(query, (name,))
        return product
    #
    # def fuzzy_search(self,name):
    #     query = f"SELECT * FROM product_table WHERE product LIKE '%{name}%'"
    #     all_products = self.fetch_all_query(query, (name,))
    #     return all_products

    #
    #
    def fuzzy_search(self,name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM product_table WHERE product LIKE '%{name}%'"
        cursor.execute(query)
        all_products = cursor.fetchall()
        return all_products


def json_creator():
    productinfo = {
                    "name": None,
                    "price": None,
                    "unit": None,
                    "quantity": None,
                    "all_price": None,
    }

    with open("product_info.json", "w") as f:
        json.dump(productinfo, f)
