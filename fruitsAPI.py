from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def send_data():
	f = open('data.json')
	data = json.load(f)
	return data 

if __name__ == "__main__":
	uvicorn.run("main:app")