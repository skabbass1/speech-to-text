import pathlib

from google.cloud import storage

def upload_audio_file_to_bucket(file_path, bucket_name):
    bucket = _get_bucket(bucket_name)
    bucket.blob(pathlib.Path(file_path).name).upload_from_filename(file_path)

def _get_bucket(bucket_name):
    client = storage.Client()
    return  client.get_bucket(bucket_name)
