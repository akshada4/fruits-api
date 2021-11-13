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
    
    def create_new(self, data):
        connect = psycopg2.connect(database=self.db_name , user=self.username , password=self.password, host=self.server , port=self.port)
        cursor = connect.cursor()
        id = data["id"]
        color = data["color"]
        fruits = data["fruits"]
        query = "INSERT INTO fruits (id, color, fruits) VALUES (%s, %s, %s)"
        data = (id, color, fruits)
        cursor.execute(query, data)
        connect.commit()
        cursor.close()
        connect.close()