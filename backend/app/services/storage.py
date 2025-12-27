import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
# import os

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    async def upload_file(self, file, file_name: str) -> str:
        try:
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                file_name
            )
            return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"
        except ClientError as e:
            raise Exception(f"Error uploading file to S3: {str(e)}")

    async def delete_file(self, file_name: str) -> bool:
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError as e:
            raise Exception(f"Error deleting file from S3: {str(e)}")