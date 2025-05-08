import sqlitecloud as sqlite
import configparser
import os

CONFIG_PATH = os.path.abspath('pages/db/config.ini')

class CustomDb:
    """Custom Database class"""
    def __init__(self, conn: object = None, group_id: str = None):
        self.conn = conn
        self.group_id = group_id.replace("-","")

    def _get_config(self, key1: str, key2: str) -> str:
        """Get the value of a key from the config file."""
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return config.get(key1, key2)
 
    def create_tables(self) -> str:
        """ create a table """
        create_tranasction_table_sql = self._get_config('query', 'create_table').format(
            self._get_config('custom_db_info', 'transaction_table').format(self.group_id),
            """transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            transaction_date TEXT, amount REAL, 
            category_name TEXT, payment_from TEXT,
            payment_to TEXT, transaction_type TEXT""")
       
        create_category_table_sql = self._get_config('query', 'create_table').format(
            self._get_config('custom_db_info', 'category_table').format(self.group_id),
            """category_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            category_name TEXT NOT NULL""")
        
        create_payment_option_table_sql = self._get_config('query', 'create_table').format(
            self._get_config('custom_db_info', 'payment_options_table').format(self.group_id),
            """payment_option_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            payment_option_name TEXT NOT NULL""")
        
        create_budget_table_sql = self._get_config('query', 'create_table').format(
            self._get_config('custom_db_info', 'budget_table').format(self.group_id),
            """budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_year TEXT NOT NULL, budget_month TEXT NOT NULL,
            budget TEXT NOT NULL""")
        
        try:
            self.conn.execute(create_tranasction_table_sql)
            self.conn.execute(create_category_table_sql)
            self.conn.execute(create_payment_option_table_sql)
            self.conn.execute(create_budget_table_sql)
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
    
    def insert_transaction_record(self, data: dict) -> str:
        """ insert a transaction record """
        try:
            insert_sql = self._get_config('query', 'insert_table').format(
                self._get_config('custom_db_info', 'transaction_table').format(self.group_id),
                "transaction_date, amount, category_name, payment_from, payment_to, transaction_type",
                "?, ?, ?, ?, ?, ?")
            self.conn.execute(insert_sql, (data["transaction_date"], data["amount"], 
                                            data["category_name"], data["payment_from"],
                                            data.get("payment_to", ""), data["transaction_type"]))                
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
    
    def insert_category_record(self, data: dict) -> str:
        """ insert a category record """
        insert_sql = self._get_config('query', 'insert_table').format(
            self._get_config('custom_db_info', 'category_table').format(self.group_id),
            "category_name",
            "?")
        
        try:
            self.conn.execute(insert_sql, (data["category_name"],))
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
    
    def insert_budget_record(self, data: dict) -> str:
        """ insert a budget record """
        insert_sql = self._get_config('query', 'insert_table').format(
            self._get_config('custom_db_info', 'budget_table').format(self.group_id),
            "budget_year, budget_month, budget",
            "?, ?, ?")
        
        try:
            self.conn.execute(insert_sql, (data["year"], data["month"], data["budget"]))
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
        
    def insert_money_source_record(self, data: dict) -> str:
        """ insert a money source record """
        insert_sql = self._get_config('query', 'insert_table').format(
            self._get_config('custom_db_info', 'payment_options_table').format(self.group_id),
            "payment_option_name",
            "?")
        
        try:
            self.conn.execute(insert_sql, (data["payment_option_name"],))
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
    
    
    def fetch_transaction_records(self, year: str, month: str) -> list | str:
        """ fetch all transaction records """
        select_sql = self._get_config('query', 'select_table_with_where').format(
            "*",
            self._get_config('custom_db_info', 'transaction_table').format(self.group_id),
            "transaction_date LIKE '%{0}%{1}\'".format(month, year))
        
        try:
            cursor = self.conn.execute(select_sql)
            result = cursor.fetchall()
            self.conn.commit()
            result = [{"transaction_id":row[0], "transaction_date":row[1], "amount":row[2], 
                           "category_name":row[3], "payment_from":row[4], "payment_to":row[5],
                           "transaction_type":row[6]} for row in result]
            return result
        except sqlite.Error as e:
            return e
    
    def fetch_category_records(self) -> list | str:
        """ fetch all category records """
        select_sql = self._get_config('query', 'select_table').format(
            "*",
            self._get_config('custom_db_info', 'category_table').format(self.group_id))
        
        try:
            cursor = self.conn.execute(select_sql)
            result = cursor.fetchall()
            self.conn.commit()
            result = [{"category_id":row[0], "category_name":row[1]} for row in result]
            return result
        except sqlite.Error as e:
            return e
    
    def fetch_payment_option_records(self) -> list | str:
        """ fetch all money source records """
        select_sql = self._get_config('query', 'select_table').format(
            "*",
            self._get_config('custom_db_info', 'payment_options_table').format(self.group_id))
        
        try:
            cursor = self.conn.execute(select_sql)
            result = cursor.fetchall()
            self.conn.commit()
            result = [{"payment_option_id":row[0], "payment_option_name":row[1]} for row in result]
            return result
        except sqlite.Error as e:
            return e
    
    def fetch_budget_record(self, data) -> list | str:
        """ fetch all budgets records for that year and month """
        select_sql = self._get_config('query', 'select_table_with_where').format(
            "*",
            self._get_config('custom_db_info', 'budget_table').format(self.group_id),
            "budget_year = ? and budget_month = ?")
        
        try:
            cursor = self.conn.execute(select_sql, (data["year"], data["month"]))
            result = cursor.fetchall()
            self.conn.commit()
            #print(result)
            result = [{"year":row[1], "month":row[2], "budget": row[3]} for row in result]
            return result
        except sqlite.Error as e:
            return e