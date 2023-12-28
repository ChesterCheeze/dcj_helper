from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

from pubmedxml import fix_xml, read_vol_issue, get_issue_id
from requestdcj import get_abstract, get_issue_by_id

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
    issue_id = get_issue_id(vol_issue['volume'], vol_issue['issue'])
    issue_data = get_issue_by_id(str(issue_id))

    return {"issueID":issue_id , "volume": vol_issue['volume'], "issue": vol_issue['issue'], "url": issue_data["articles"][0]["publications"][0]["_href"]}


@app.post("/download")
def download_file():
    return FileResponse("modified_file_1.xml", media_type="application/xml", filename="modified_file_1.xml")
