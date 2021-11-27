from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from src.databaseSetup import Operation

class NewData(BaseModel):
	color: str
	fruits: List[str]

class UpdateData(BaseModel):
	fruits: List[str]

app = FastAPI()
operation = Operation()

@app.get("/",status_code=200)
def get_data(color: Optional[str] = None):
	if (color):
		data = operation.get_data("color",color)
		if (data):
			return data
		
		raise HTTPException(status_code=404, detail="item not found")
	else:
		data = operation.get_all()
		return data

@app.get("/{id}",status_code=200)
def get_data_by_id(id: int):
	data = operation.get_data("id",id)

	if (data):
		return data

	raise HTTPException(status_code=404, detail="item not found")

@app.post("/fruits")
def create(newData: NewData):
	data = {"color": newData.color, "fruits": newData.fruits}
	return operation.create_new(data)

@app.put("/update-fruits/{color}")
def update(updatedData: UpdateData, color: str):
	data = {"color": color, "fruits": updatedData.fruits}
	print(data)
	return operation.put_data(color, updatedData.fruits)

# if __name__ == "__main__":
# 	uvicorn.run("fruitsAPI:app", host="0.0.0.0", port=5000, reload=True)