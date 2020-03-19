import os
from typing import List


def clean_files(file_names:List[str]):
    for file_name in file_names:
        os.remove(file_name)
