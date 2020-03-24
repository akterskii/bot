import os

from main_logic.common_const.common_const import IMAGE_STORAGE
from main_logic.google_cloud.clients import StorageClient


def upload_to_bucket(file_path: str) -> str:
    file_base_name = os.path.basename(file_path)
    storage_client = StorageClient().get_client()
    bucket = storage_client.bucket(bucket_name=IMAGE_STORAGE)
    blob = bucket.blob(file_base_name)
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url
