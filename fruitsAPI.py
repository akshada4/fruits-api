from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import uvicorn
from databaseSetup import Operation

class NewData(BaseModel):
	id: int
	color: str
	fruits: List[str]

app = FastAPI()
operation = Operation()

def read_json():
	f = open('data.json')
	return json.load(f)

@app.get("/",status_code=200)
def get_data():
	data = operation.get_all()
	return data

@app.get("/{id}",status_code=200)
def get_data(id: int):
	data = read_json()

	for i in data:
		if i["id"] == id:
			return i

	raise HTTPException(status_code=404, detail="item not found")

@app.post("/fruits")
def create(newData: NewData):
	data = {"id": newData.id, "color": newData.color, "fruits": newData.fruits}
	operation.create_new(data)
	return newData

if __name__ == "__main__":
	uvicorn.run("fruitsAPI:app")