from botocore.client import Config
from storages.backends.s3boto3 import S3Boto3Storage

class PublicImagesStorage(S3Boto3Storage):
    location = 'images'
    default_acl = 'public-read'
    file_overwrite = False
    config = Config(signature_version='s3v4')
