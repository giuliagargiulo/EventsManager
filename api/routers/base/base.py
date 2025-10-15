from fastapi import APIRouter
import os

BASE_DIR = os.getenv("BASE_DIR", "/app")
FILES_DIR = os.getenv("FILES_DIR", "/app/files")

router = APIRouter(tags=["base"])

@router.get("/",
            summary="Root Endpoint",
            description="Return a welcome message",
            response_description="A welcome message in JSON format")
def root():
    return {"message": "Welcome to the Events Manager API!"}

@router.get("/greet",
            summary="Greet Endpoint",
            description="Return a, welcome message for the user",
            response_description="A personalised welcome message in JSON format")
def greet_user(name:str):
    return {"message" : f"Hello {name}, welcome to the Events Manager API!"}

# convert CSV to TXT
@router.post("/convert-file",
             summary="Convert CSV to TXT",
             description="Convert a CSV file to a TXT file",
             response_description="A message indicating the result of the conversion operation")
def convert_csv_to_txt():
    csv_file_path = os.path.join(FILES_DIR, "events.csv")
    txt_file_path = os.path.join(FILES_DIR, "events.txt")
    with open(csv_file_path, "r") as csv_f, open(txt_file_path, "a") as txt_f:
        for line in csv_f:
            txt_f.write(line.replace(",", " "))
    return {"message": "CSV file converted to TXT successfully."}
