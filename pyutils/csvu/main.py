import os
import csv
from pyutils.logu.main import logger

import itertools


class CsvDictStream:
    def __init__(self, filename, fieldnames, mode="w"):
        if not os.path.exists(filename):
            mode = "w"
        self.fp = open(filename, mode)
        self.fieldnames = fieldnames
        self.writer = csv.DictWriter(self.fp, fieldnames=fieldnames)
        if mode == "w":
            self.writer.writeheader()

    def writerows(self, rows):
        self.writer.writerows(rows)

    def writerow(self, row):
        self.writer.writerow(row)

    def __del__(self):
        self.close()

    def close(self):
        try:
            if self.fp.closed:
                return
            self.fp.close()
        except Exception:
            pass



def lower_first(iterator):
    return itertools.chain([next(iterator).lower()], iterator)


def load_csv(
    file_path,
    skip_func=None,
    key=None,
    row_func=None,
    lowercase_header=False,
    group=False,
):
    data = []
    if key is not None:
        data = {}
    logger.debug("loading csv file: {}".format(file_path))
    if not os.path.exists(file_path):
        return data
    headers = None
    with open(file_path) as fp:
        headers = next(csv.reader(fp))
    if lowercase_header:
        headers = [header.lower() for header in headers]
    with open(file_path) as fp:
        reader = csv.DictReader(fp, fieldnames=headers)
        # skip header row
        next(reader)
        for row in reader:
            if callable(skip_func) and skip_func(row):
                continue
            data_keys = None
            if key is None:
                pass
            elif isinstance(key, str):
                data_keys = row.get(key)
            elif isinstance(key, (tuple, list)):
                data_keys = tuple(row.get(k) for k in key)
            else:
                raise Exception(f"Invalid key type: {type(key)}: {key}")
            if callable(row_func):
                row = row_func(row)
            if isinstance(data, list):
                data.append(row)
            else:
                if group:
                    v = data.get(data_keys)
                    if v:
                        data[data_keys].append(row)
                    else:
                        data[data_keys] = [row]
                else:
                    data[data_keys] = row
    logger.debug("loaded csv file: {} with rows: {}".format(file_path, len(data)))
    return data


def save_csv(file_path, rows, mode, fieldnames=None):
    logger.debug("Saving csv file: {}, rows: {}".format(file_path, len(rows)))
    if not rows:
        return
    if isinstance(rows, dict):
        rows = list(rows.values())
    if isinstance(rows, dict) and fieldnames is None:
        fields = set()
        for key in rows:
            fields.add(key)
        fieldnames = list(fields)
    write_header = False
    if not os.path.exists(file_path) or mode == "w":
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        write_header = True
    with open(file_path, mode) as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames or rows[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(rows)
