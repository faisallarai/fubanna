import os
import random


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)

    return name, ext


def get_image_path(instance, filename):
    new_filename = random.randint(1, 9387678978734)
    name, ext = get_filename_ext(filename)
    print(name)
    final_filename = f'{new_filename}{ext}'

    return f'products/{new_filename}/{final_filename}'
