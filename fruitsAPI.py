from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

class NewData(BaseModel):
	id: int
	color: str
	fruits: List[str]

app = FastAPI()

def read_json():
	f = open('data.json')
	return json.load(f)

@app.get("/",status_code=200)
def get_data():
	data = read_json()
	return data

@app.get("/{id}",status_code=200)
def get_data(id: int):
	data = read_json()

	for i in data:
		if i["id"] == id:
			return i

	raise HTTPException(status_code=404, detail="item not found")

@app.post("/create")
def create_data(data: NewData):
	return data


if __name__ == "__main__":
	uvicorn.run("main:app")