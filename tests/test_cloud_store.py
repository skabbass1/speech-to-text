from unittest import mock

import pytest
import cloud_store

def test_upload_audio_file_to_bucket(monkeypatch):
    from google.cloud import storage

    monkeypatch.setattr(storage.Client, 'get_bucket', mock.MagicMock())
    breakpoint()
    cloud_store.upload_audio_file_to_bucket('', '')
    pass



