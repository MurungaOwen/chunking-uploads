"""module to handle chunking and merging at the server"""
from fastapi import UploadFile
from uuid import uuid4
from config import app_config


async def upload_to_s3(file: UploadFile) -> str:
    """
    Uploads a file to S3 in chunks.
    
    Args:
        file (UploadFile): The file to upload.
    """
    # Placeholder for actual S3 upload logic
    chunk_count = 0
    s3 = app_config.s3
    
    # Simulate chunking and uploading

    # setup multipart upload
    file_key = f"uploads/{uuid4()}_{file.filename}"

    multipart_upload = s3.create_multipart_upload(
        Key=file_key,
        Bucket=app_config.BUCKET_NAME
    )
    upload_id = multipart_upload['UploadId']
    chunk_count = 1
    parts = []
    try:
        while True:
            chunk = await file.read(app_config.CHUNK_SIZE)
            if not chunk:
                break

            part_upload_response = s3.upload_part(
                Bucket=app_config.BUCKET_NAME,
                Key=file_key,
                PartNumber=chunk_count,
                UploadId=multipart_upload['UploadId'],
                Body=chunk
            )
            parts.append({ # type: ignore
                "PartNumber": chunk_count,
                "ETag": part_upload_response["ETag"]
            })
            chunk_count += 1
        s3.complete_multipart_upload(
            Bucket=app_config.BUCKET_NAME,
            Key=file_key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': app_config.BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=3600
        )
        return url
    except Exception as e:
        s3.abort_multipart_upload(
            Bucket=app_config.BUCKET_NAME,
            Key=file_key,
            UploadId=upload_id
        )
        raise e


        