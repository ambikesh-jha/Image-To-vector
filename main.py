from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
from typing import List
from vector_converter import VectorConverter  # Assuming VectorConverter is in a separate file

app = FastAPI()

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates for HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_files(
    request: Request,
    files: List[UploadFile] = File(...),
    format: str = Form(...)
):
    # Create a temporary directory to store uploaded files
    input_folder = Path("uploaded_images")
    input_folder.mkdir(exist_ok=True)

    # Save uploaded files
    for file in files:
        file_path = input_folder / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

    # Convert files
    converter = VectorConverter()
    output_folder = Path("result_vector")
    output_folder.mkdir(exist_ok=True)
    converted_files = converter.convert(
        input_path=str(input_folder),
        output_format=format,
        output_folder=str(output_folder)
    )

    # Clean up uploaded files
    for file in input_folder.iterdir():
        os.remove(file)

    # Prepare file URLs for display
    file_urls = [f"/download/{Path(file).name}" for file in converted_files]

    return JSONResponse({"file_urls": file_urls})

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = Path("result_vector") / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    
    return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)