import sqlitecloud as sqlite
import configparser
import os

CONFIG_PATH = os.path.abspath('pages/db/config.ini')

class UserInfoDB:
    """User Info Database class"""
    def __init__(self, conn: object = None):
        self.conn = conn

    def _get_config(self, key1: str, key2: str) -> str:
        """Get the value of a key from the config file."""
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return config.get(key1, key2)
        
    def create_login_table(self):
        """ create a login table """
        create_table_sql = self._get_config('query', 'create_table').format(
            self._get_config('user_info', 'login_table'),
            "username TEXT PRIMARY KEY, password TEXT NOT NULL")
        
        try:
            self.conn.execute(create_table_sql)
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
        
    def create_group_user_table(self):
        """ create a group table """
        create_table_sql = self._get_config('query', 'create_table').format(
            self._get_config('user_info', 'group_user_table'),
            "group_id TEXT, username TEXT, FOREIGN KEY(username) REFERENCES login(username)")
        
        try:
            self.conn.execute(create_table_sql)
            self.conn.commit()
            return "Success"
        except sqlite.Error as e:
            return e
        
    def _check_username_exist(self, username, return_bool=False) -> bool | tuple | str:
        """ check if the username is exist """
        select_sql = self._get_config('query', 'select_table_with_where').format(
            "*",
            self._get_config('user_info', 'login_table'),
            "username = ?")
        
        try:
            cursor = self.conn.execute(select_sql, (username,))
            result = cursor.fetchone()
            self.conn.commit()
            if return_bool:
                return result is not None and username in result
            else:
                return result
        except sqlite.Error as e:
            return e

    def insert_user(self, data: dict) -> dict | str:
        """ insert a new user into the login table and group table """
        try:
            if self._check_username_exist(data["username"], return_bool=True):
                raise ValueError("Username already exists")
            
            insert_sql = self._get_config('query', 'insert_table').format(
                self._get_config('user_info', 'login_table'),
                "username, password",
                "?, ?")
            self.conn.execute(insert_sql, (data["username"], data["password"]))
            result_data = self._check_username_exist(data["username"])

            insert_group_sql = self._get_config('query', 'insert_table').format(
                self._get_config('user_info', 'group_user_table'),
                "group_id, username",
                "?, ?")
            self.conn.execute(insert_group_sql, (data["group_id"], result_data[0]))
            self.conn.commit()
            
            return [{
                "username": result_data[0],
                "group_id": data["group_id"]
            }]
        except sqlite.Error as e:
            return e
        except Exception as e:
            return e

    def fetch_user(self, data: dict) -> dict | str:
        """ fetch user data from the login and group table """
        
        try:
            result_data =  self._check_username_exist(data["username"])
            #print("check1"+ str(result_data))
            if result_data is None or result_data == ():
                raise Exception("User not found")
            
            select_sql = self._get_config('query', 'select_table_with_where').format(
                "*",
                self._get_config('user_info', 'group_user_table'),
                "username = ?")
            cursor = self.conn.execute(select_sql, (result_data[0],))
            group_result_data = cursor.fetchone()
            self.conn.commit()

            return [{
                "username": result_data[0],
                "group_id": group_result_data[0]
            }]
        except sqlite.Error as e:
            return e
        except Exception as e:
            return e

    def fetch_group_users(self, group_id: str) -> dict | str:
        """ fetch all users in a group """
        select_sql = self._get_config('query', 'select_table_with_where').format(
            "*",
            self._get_config('user_info', 'group_user_table'),
            "group_id = ?")
        
        try:
            cursor = self.conn.execute(select_sql, (group_id,))
            result = cursor.fetchall()
            self.conn.commit()
            result_dict = [{"username": row[1], "group_id": row[0]} for row in result]
            return result_dict
        except sqlite.Error as e:
            return e
        except Exception as e:
            return e
    
    def close(self):
        """ close the database connection """
        if self.conn:
            self.conn.close()
    
    