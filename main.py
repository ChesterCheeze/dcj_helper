from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
from pubmedxml import fix_xml, read_vol_issue

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
async def create_upload_file(file_upload: UploadFile):
    data_byte = await file_upload.read()
    
    data_str = data_byte.decode()
    vol_issue = read_vol_issue(data_str)
    
    return {"volume": vol_issue['volume'], "issue": vol_issue['issue']}


@app.post("/download")
def download_file():
    return FileResponse("modified_file_1.xml", media_type="application/xml", filename="modified_file_1.xml")
