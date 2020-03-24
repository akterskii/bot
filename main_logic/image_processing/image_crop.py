from typing import List, Tuple

from PIL import Image


class ScaledFactors:
    factors = [0.6, 0.4]
    min_width = 300
    min_height = 300


def crop_images(file_name: str) -> List[Tuple[str, float]]:
    """Returns list of files names"""
    base_image = Image.open(file_name)
    width, height = base_image.size

    small_images_file_names = [(file_name, 1.)]
    for factor in ScaledFactors.factors:
        delta_x = int(width * factor)
        delta_y = int(height * factor)
        offset_x = (width - delta_x) // 2
        offset_y = (width - delta_y) // 2
        parts = file_name.split('.')
        part_name = parts[0] + str(factor) + '.' + parts[1]
        base_image.crop(
            (offset_x, offset_y, delta_x + offset_x, delta_y + offset_y)
        ).save(part_name)
        small_images_file_names.append((part_name, factor))

    return small_images_file_names

