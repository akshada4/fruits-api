FROM python:3.8.10
WORKDIR /fruitsapi
COPY ./requirements.txt /fruitsapi/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /fruitsapi/requirements.txt
COPY src /fruitsapi/src
# CMD ["python3",  "/fruitsapi/src/fruitsAPI.py"]
CMD ["uvicorn", "src.fruitsAPI:app", "--host", "0.0.0.0", "--port", "5000"]