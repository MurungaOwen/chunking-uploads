from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services.file import upload_to_s3


def create_app():
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )
    return app


app = create_app()

@app.get("/") # type: ignore
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/upload") # type: ignore
async def upload_file(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, size: {file.size / 1000000} megabytes") # type: ignore
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        file_url = await upload_to_s3(file) # type: ignore
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded and processed successfully",
                "live_url": file_url,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
