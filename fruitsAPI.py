from fastapi import FastAPI
import json

app = FastAPI()

def read_json():
	f = open('data.json')
	return json.load(f)

@app.get("/")
def get_data():
	data = read_json()
	return data

@app.get("/{id}")
def get_data(id: int):
	data = read_json()
	for i in data:
		if i["id"] == id:
			return i
		else:
			return {}



if __name__ == "__main__":
	uvicorn.run("main:app")