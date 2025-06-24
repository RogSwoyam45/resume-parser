import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pypdf import PdfReader
from resumeparser import ats_extractor

app = FastAPI()

UPLOAD_PATH = "__DATA__"
os.makedirs(UPLOAD_PATH, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <body>
            <h2>Upload Resume PDF</h2>
            <form action="/process" enctype="multipart/form-data" method="post">
                <input name="pdf_doc" type="file" accept="application/pdf">
                <input type="submit">
            </form>
        </body>
    </html>
    """

@app.post("/process")
async def ats(pdf_doc: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_PATH, "file.pdf")
    with open(file_location, "wb") as f:
        f.write(await pdf_doc.read())
    data = _read_file_from_path(file_location)
    result = ats_extractor(data)
    return JSONResponse(content=result)

def _read_file_from_path(path):
    reader = PdfReader(path)
    data = ""
    for page in reader.pages:
        data += page.extract_text()
    return data