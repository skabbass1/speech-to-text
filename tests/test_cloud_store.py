from unittest import mock

import pytest
import cloud_store

# TODO: This should be a proper integration test. Currently google
# does not provide a simulated object store for local testing.
def test_upload_audio_file_to_bucket(monkeypatch):
    from google.cloud import storage
    monkeypatch.setattr(storage.Client, 'get_bucket', mock.MagicMock())
    cloud_store.upload_audio_file_to_bucket('/some/file', 'some_bucket')
