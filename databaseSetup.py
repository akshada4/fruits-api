import psycopg2
import os
from dotenv import load_dotenv

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

        query = "INSERT INTO fruits (color, fruits) VALUES (%s, %s);"
        data = (color, fruits)
        cursor.execute(query, data)
        connect.commit()

        self.close_connection(connect, cursor)

    def get_all(self):
        [connect, cursor] = self.setup_connection()

        query = "SELECT * from fruits;"
        cursor.execute(query)
        data = cursor.fetchall()
        connect.commit()

        self.close_connection(connect, cursor)

        json_data = self.convert_to_json(data)
        return json_data
    

        