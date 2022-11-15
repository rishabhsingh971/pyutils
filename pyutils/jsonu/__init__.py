import os
import json
from logu import logger

def load_json(file_path):
    logger.debug('load json: {}'.format(file_path))
    if not os.path.isfile(file_path):
        return {}
    with open(file_path) as fp:
        return json.load(fp)


def save_json(file_path, data, **kwargs):
    logger.debug('saving json: {}'.format(file_path))
    parent_dir = os.path.dirname(file_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    with open(file_path, "w") as fp:
        json.dump(data, fp, **kwargs)

