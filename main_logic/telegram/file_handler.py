from typing import Dict

from envs.poseenv.Lib import os

from main_logic.common_const.common_const import QUEST_STAGES
from main_logic.google_cloud.clients import DatastoreClient
from main_logic.google_cloud.file_management import upload_to_bucket
from main_logic.image_processing.image_crop import crop_images


def process_and_upload_image(stage_id: str, base_image_path: str):
    file_names_and_factors = crop_images(base_image_path)

    factors_to_data: Dict[float, Dict[str, str]] = {}
    for file_path, factor in file_names_and_factors:
        public_link = upload_to_bucket(file_path=file_path)
        base_file_name = os.path.basename(file_path)
        factors_to_data[factor] = {
            'file_name': base_file_name,
            'url': public_link
        }

    db_client = DatastoreClient().get_client()
    db_client.collection(QUEST_STAGES).document(stage_id).update(
        {'images': factors_to_data})
