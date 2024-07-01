import psycopg2 as pg
import pandas as pd

class Products:
    """Managing data from the 'products' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="computer_shop",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.products_df = None
        
    def products_loading(self):
        """Refreshing the 'products' table data."""
        
        self.products_df = pd.read_sql_query("SELECT * FROM products",
                                             self.con)
    
    def products_entry_data(self, sql):
        """Entering values in the 'products' table."""

        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()

        # The connection will be closed with the application.
        curs.close()

        self.products_loading()


class Sale:
    """Managing data from the 'sale' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="computer_shop",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.sale_df = None
    
    def sale_loading(self):
        """Refreshing the 'sale' table data."""
        
        self.sale_df = pd.read_sql_query("SELECT * FROM sale", self.con)
    
    def sale_entry_data(self, sql):
        """Entering values in the 'sale' table."""
        
        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()
        
        # The connection will be closed with the application.
        curs.close()
        
        self.sale_loading()


class Orders:
    """Managing data from the 'orders' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="computer_shop",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.orders_df = None
    
    def orders_loading(self):
        """Refreshing the 'orders' table data."""
        
        self.orders_df = pd.read_sql_query("SELECT * FROM orders", self.con)
    
    def orders_entry_data(self, sql):
        """Entering values in the 'orders' table."""
        
        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()
        
        # The connection will be closed with the application.
        curs.close()
        
        self.orders_loading()


class OrderItems:
    """Managing data from the 'order_items' table."""
    
    def __init__(self):
        self.con = pg.connect(
            database="computer_shop",
            user="postgres",
            password="pg11kdk",
            host="localhost",
            port="5433"
        )
        self.order_items_df = None
    
    def order_items_loading(self):
        """Refreshing the 'order_items' table data."""
        
        self.order_items_df = pd.read_sql_query("SELECT * FROM order_items",
                                                self.con)
    
    def order_items_entry_data(self, sql):
        """Entering values in the 'order_items' table."""
        
        curs = self.con.cursor()
        curs.execute(sql)
        self.con.commit()
        
        # The connection will be closed with the application.
        curs.close()
        
        self.order_items_loading()


products = Products()
products.products_loading()
sale = Sale()
sale.sale_loading()
orders = Orders()
orders.orders_loading()
order_items = OrderItems()
order_items.order_items_loading()
