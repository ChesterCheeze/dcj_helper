from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
from pubmedxml import modify_file

with open("api_key.json") as f:
    data = json.load(f)

API_KEY = data["api_key"]

UPLOAD_FOLDER = Path() / "uploads"

app = FastAPI()

# defining a route
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/index", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/index")
def create_upload_file(file_upload: UploadFile):
    data = file_upload.read()
    #save_to = UPLOAD_FOLDER / file_upload.filename
    #with open(save_to, "wb") as buffer:
    #    buffer.write(data)
    vol_issue = modify_file(data)
    #return templates.TemplateResponse("index.html",{"filename": file_upload.filename, "request": request})
    return {"volume": vol_issue['volume'], "issue": vol_issue['issue']}


@app.post("/download")
def download_file():
    return FileResponse("modified_file_1.xml", media_type="application/xml", filename="modified_file_1.xml")
