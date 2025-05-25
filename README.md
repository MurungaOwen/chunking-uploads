# Python Threading FastAPI S3 Uploader

This project is a FastAPI application for uploading filesin chunks, in the `main` branch we use directory and in `s3-integration` branch we use s3 buckets to store the files.supporting large file uploads with multipart upload. It is designed for extensibility and ease of use.

## Project Structure

- `app.py` — Main FastAPI application, exposes endpoints for file upload.
- `config.py` — Configuration for AWS S3 and chunk size, using environment variables.
- `services/` — Contains logic for file chunking and S3 upload.
  - `file.py` — Handles chunked upload and S3 multipart logic.
- `typings/` — Type stubs for dependencies (for type checking).
- `env/` — Python virtual environment (not included in version control).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MurungaOwen/chunking-uploads.git
cd python-threading
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv env
source env/Scripts/activate  # On Windows
```

### 3. Install Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following content:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=your-region
S3_BUCKET_NAME=your-bucket-name
```

### 5. Run the Application
```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

- `GET /` — Health check endpoint.
- `POST /upload` — Upload a file (multipart/form-data, field name: `file`).

## Notes
- Make sure your AWS credentials and bucket permissions are set correctly.
- The upload logic uses chunked multipart upload for efficiency with large files.
- Type stubs are provided for better type checking and IDE support.
