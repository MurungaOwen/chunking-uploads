from config import app_config
from fastapi import UploadFile
import os
import shutil
import uuid

def create_storage_dirs() -> None:
    os.makedirs(app_config.CHUNK_DIR, exist_ok=True)
    os.makedirs(app_config.COMPLETED_DIR, exist_ok=True)
    return

async def upload_chunks(file: UploadFile) -> tuple[int, uuid.UUID]:
    """divide to chunks and upload each to the ```tmp/file_id``` folder"""
    file_id = uuid.uuid4()
    create_storage_dirs()

    chunk_folder = os.path.join(app_config.CHUNK_DIR, f"{file_id}")
    chunk_number = 0

    os.makedirs(chunk_folder, exist_ok=True)

    try:
        while True:
            chunk = await file.read(app_config.CHUNK_SIZE)
            if not chunk: # type: ignore
                break

            chunk_path = os.path.join(chunk_folder, f"{chunk_number}")
            with open(chunk_path, "wb") as chunk_file:
                chunk_file.write(chunk) # type: ignore
            chunk_number += 1
        return chunk_number, file_id
    except Exception as e:
        print(f"Error processing file {file.filename}: {e}")
        raise e


def merge_chunks(original_filename: str, file_id: uuid.UUID, chunk_count: int) -> str:
    chunk_folder = os.path.join(app_config.CHUNK_DIR, f"{file_id}")
    os.makedirs(app_config.COMPLETED_DIR, exist_ok=True)

    temp_path = os.path.join(app_config.COMPLETED_DIR, f"{file_id}.tmp")
    final_path = os.path.join(app_config.COMPLETED_DIR, original_filename)

    with open(temp_path, "wb") as final_file:
        for i in range(chunk_count):
            chunk_path = os.path.join(chunk_folder, f"{i}")
            with open(chunk_path, "rb") as chunk_file:
                shutil.copyfileobj(chunk_file, final_file)

    shutil.rmtree(chunk_folder)
    os.rename(temp_path, final_path)
    return final_path



