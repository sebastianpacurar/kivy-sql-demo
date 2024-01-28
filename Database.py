from decouple import config
import mysql.connector


class Database:
    def __init__(self):
        self.tables = []
        self.curr_table = None
        self.curr_db = None
        self.host = config('DB_HOST')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')

        self.init_app_start()

    def set_conn(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.curr_db
        )

    def get_all_dbs(self):
        """ return all mysql dbs, excepting the default ones """
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            db_names = [x[0] for x in cursor.fetchall()]
            exclusions = ['information_schema', 'performance_schema', 'sys', 'world', 'mysql']
            db_formatted = [db for db in db_names if db not in exclusions]
            return db_formatted

    def get_all_tables(self):
        """ get all tables from current db """
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            parsed = [x[0] for x in cursor.fetchall()]
            return parsed

    def get_all_cols(self):
        """ get all columns of a table """
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.curr_table}")
            return cursor.fetchall()

    def get_table_cols_list(self):
        """ get all table columns as list"""
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {self.curr_table}")
            return [x[0] for x in cursor.fetchall()]

    def set_table(self, target):
        self.curr_table = target

    def set_tables(self):
        self.tables = self.get_all_tables()
        self.set_table(self.tables[0])

    def set_db(self, target):
        """ set current db - performed when switching tabs """
        self.curr_db = target
        self.set_tables()

    def init_app_start(self):
        self.curr_db = self.get_all_dbs()[0]
        self.curr_table = self.get_all_tables()[0]
