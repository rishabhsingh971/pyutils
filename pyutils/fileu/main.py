import os
from pyutils.logu.main import logger
from pyutils.csvu import load_csv, save_csv
from math import ceil


def get_dirs(prefix_path: str, ignore_hidden=True):
    parent = os.path.dirname(prefix_path)
    prefix = os.path.basename(prefix_path)
    if not parent:
        parent = "."
    result = []
    for fname in os.listdir(parent):
        fpath = os.path.join(parent, fname)
        if not fname.startswith(prefix) or not os.path.isdir(fpath):
            continue
        if ignore_hidden and fname.startswith("."):
            continue
        result.append(fpath)
    return result


def get_files(
    dir_paths, prefix: bool = False, recursive=False, ignore_hidden=True, is_valid=None
):
    if isinstance(dir_paths, str):
        dir_paths = [dir_paths]
    if prefix:
        new_dir_paths = []
        for dir_path in dir_paths:
            new_dir_paths.extend(get_dirs(dir_path))
        dir_paths = new_dir_paths
    file_paths = []
    for dir_path in dir_paths:
        for fname in os.listdir(dir_path):
            fpath = os.path.join(dir_path, fname)
            if callable(is_valid) and not is_valid(fname, fpath):
                continue
            if os.path.isdir(fpath) and recursive:
                if ignore_hidden and fname.startswith("."):
                    continue
                file_paths.extend(get_files(fpath, prefix=False, recursive=True))
            if os.path.isfile(fpath):
                file_paths.append(fpath)
    return file_paths


def merge_csv(file_paths, key=None, skip_func=None):
    all_rows = []
    if key:
        all_rows = {}
    for file_path in file_paths:
        rows = load_csv(file_path, key=key, skip_func=skip_func)
        logger.debug("File : {} : {}".format(file_path, len(rows)))
        if key:
            all_rows.update(rows)
        else:
            all_rows.extend(rows)
    logger.debug("Total: {}".format(len(all_rows)))
    return all_rows


def split_csv(file_path, files_split=None, rows_split=500000):
    logger.info("Reading: {}".format(file_path))
    rows = load_csv(file_path)
    logger.info("Found: {} rows".format(len(rows)))
    if files_split:
        rows_split = ceil(len(rows) / files_split)
    if not rows_split:
        return
    splits = file_path.split(".")
    file_path_without_extension, extension = ".".join(splits[:-1]), splits[-1]
    new_file_path = "%s_{}.%s" % (file_path_without_extension, extension)
    for i, k in enumerate(range(0, len(rows), rows_split)):
        logger.info("Save : {}".format(new_file_path.format(i + 1)))
        end = min(k + rows_split, len(rows))
        save_csv(new_file_path.format(i + 1), rows[k:end], "w")

