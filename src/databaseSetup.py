import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import sql

class Setup():
    def __init__(self):
        load_dotenv()
        self.username =  os.getenv("POSTGRES_USER")
        self.password = os.getenv("PASSWORD")
        self.port = os.getenv("PORT")
        self.server = os.getenv("SERVER")
        self.db_name = os.getenv("DB_NAME")

    def setup_connection(self):
        connect = psycopg2.connect(database=self.db_name , user=self.username , password=self.password, host=self.server , port=self.port)
        cursor = connect.cursor()
        return [connect, cursor]
    
    def close_connection(self, cursor, connect):
        cursor.close
        connect.close()

    def convert_to_json(self, data):
        all_data = []

        for i in data:
            dict_data = {"id": i[0], "color": i[1], "fruits": i[2]}
            all_data.append(dict_data)

        return all_data


class Operation(Setup):    
    def create_new(self, data):
        [connect, cursor] = self.setup_connection()

        color = data["color"]
        fruits = data["fruits"]

        data_exists = cursor.execute("SELECT EXISTS (SELECT 1 from fruits WHERE color = (%s));", (color,))

        if (not data_exists):
            query = "INSERT INTO fruits (color, fruits) VALUES (%s, %s);"
            posted_data = (color, fruits)
            cursor.execute(query, posted_data)
            connect.commit()

        returned_data = data if not data_exists else  {"err": "color already exists"}
        self.close_connection(connect, cursor)
        return returned_data

    def get_all(self):
        [connect, cursor] = self.setup_connection()

        query = "SELECT * from fruits;"
        cursor.execute(query)
        data = cursor.fetchall()

        self.close_connection(connect, cursor)

        json_data = self.convert_to_json(data)
        return json_data
    
    def get_data(self, parameter_name, parameter):
        [connect, cursor] = self.setup_connection()
        query = sql.SQL("SELECT * from fruits WHERE {} = (%s);").format(sql.Identifier(parameter_name))

        try:
            cursor.execute(query,(parameter,))
            data = cursor.fetchone()
            self.close_connection(connect, cursor)
            return self.convert_to_json([data])[-1]
        except:
           return None  

    def put_data(self, color, data):
        [connect, cursor] = self.setup_connection()
        update_query = "UPDATE fruits SET fruits = fruits || (%s) WHERE color = (%s)"
        cursor.execute(update_query,(data,color))
        connect.commit()
        
        fetch_query = cursor.execute("SELECT * from fruits WHERE color = (%s);", (color,))
        updated_entry = cursor.fetchone()
        
        self.close_connection(connect, cursor)

        json_data = self.convert_to_json([updated_entry])[-1]
        return  json_data