import boto3
from mypy_boto3_s3 import S3Client

s3: S3Client = boto3.client( # type: ignore
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='us-east-1'
    bucket_name='YOUR_BUCKET_NAME'
)

class AppConfig():
    def __init__(self):
        self.s3 = s3
        self.CHUNK_SIZE = 1024 * 1024 * 1  # 1 MB
        self.BUCKET_NAME = ""

app_config = AppConfig()

