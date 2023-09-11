import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

from google.cloud import storage

GCS_CREDENTIAL_FILE_PATH="GCS_CREDENTIAL_FILE_PATH"

class GCSConnector:
    def __init__(
        self, bucket_name, credential_file_path=None,
    ):
        if credential_file_path is None:
            credential_file_path = os.getenv(GCS_CREDENTIAL_FILE_PATH)
        client = storage.Client.from_service_account_json(credential_file_path)
        self.bucket = client.get_bucket(bucket_name)

    def unread_blobs(self, dir_prefix, blob_names_read):
        blobs = []
        for blob in self.get_blobs(dir_prefix):
            name = blob.name
            if name not in blob_names_read:
                blobs.append(blob)
        return blobs

    def get_blobs(self, dir_prefix, remove_bucket_name=False):
        if remove_bucket_name:
            prefix = f"gs://{self.bucket}/"
            if dir_prefix.startswith(prefix):
                dir_prefix = dir_prefix[len(prefix) :]
        return self.bucket.list_blobs(prefix=dir_prefix)

    @staticmethod
    def blob_to_string(blob):
        return blob.download_as_string()

    @staticmethod
    def download_blob(blob, path=None, overwrite=False):
        if not path:
            path = blob.path.split("/o/")[1].replace("%2F", os.path.sep)

            parent = os.path.dirname(path)
            if not os.path.exists(parent):
                os.makedirs(parent)

        if os.path.exists(path) and not overwrite:
            # print("path exists %s" % path)
            return path
        blob.download_to_filename(path)
        return path

    def download_dir(self, dir_prefix):
        blobs = self.get_blobs(dir_prefix)
        self.download_blobs_multithreaded(blobs)

    @staticmethod
    def download_dir_gsutil(dir_prefix, path="."):
        dir_prefix = '"%s"' % dir_prefix
        path = '"%s"' % path
        return subprocess.run(
            ["gsutil", "-m", "cp", "-r", dir_prefix, path], check=True
        )

    @staticmethod
    def download_blobs_multithreaded(blobs):
        start = time.time()
        with ThreadPoolExecutor() as executor:
            executor.map(GCSConnector.download_blob, blobs)
        delta = time.time() - start
        # print("%d items downloaded in %ds" % (len(blobs), delta))

    @staticmethod
    def download_blobs(blobs):
        start = time.time()
        for blob in blobs:
            GCSConnector.download_blob(blob)
        delta = time.time() - start
        # print("%d items downloaded in %ds" % (len(blobs), delta))

    def upload_file(self, src, dst=None, make_public=False):
        if not os.path.exists(src):
            return False
        if dst is None:
            dst = src
        blob = self.bucket.blob(dst)
        blob.upload_from_filename(src)
        if make_public:
            blob.make_public()
            return blob.public_url
        return True

    def download_file(self, src, dst):
        blob = self.bucket.get_blob(src)
        if not blob:
            return False
        parent_dir = os.path.dirname(dst)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        blob.download_to_filename(dst)
        return True
