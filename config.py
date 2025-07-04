import boto3
from mypy_boto3_s3 import S3Client
from decouple import config  # type: ignore

s3: S3Client = boto3.client( # type: ignore
    's3',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID', ""),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY', ""),
    region_name=config('AWS_REGION', ""),
    bucket_name=config('S3_BUCKET_NAME', "")
)

class AppConfig():
    def __init__(self):
        self.s3 = s3
        self.CHUNK_SIZE = 1024 * 1024 * 1  # 1 MB
        self.BUCKET_NAME = config('S3_BUCKET_NAME', "")

app_config = AppConfig()

