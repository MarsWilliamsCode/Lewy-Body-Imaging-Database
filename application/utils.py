import boto3
from django.conf import settings
from .models import Image
def upload_image_to_s3(image_file, image_id, scan_id, object_key):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Upload the file
    s3_client.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, object_key, ExtraArgs={'ACL': 'public-read'})

    # Create the public URL
    s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{object_key}"

    # Save the URL to the database
    image = Image(image_id=image_id, scan_id_id=scan_id, image_url=s3_url)
    image.save()
    return s3_url
