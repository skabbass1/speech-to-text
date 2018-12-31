from dataclasses import dataclass

import pytest

import transcriber

def test_build_request_payload(audio_file_uri):
    """
    it correctly builds the request payload
    """
    got = transcriber._build_request_payload(audio_file_uri)
    expected = {
        'config': {'languageCode': 'en-US'},
        'audio': {'uri': audio_file_uri}
    }

    assert got == expected

def test_submit_for_recognition(audio_file_uri, monkeypatch):
    """
    it makes a post request to  long running recognize uri
    """
    import requests
    def mock_post(uri, json, params):
        return _MockResponse(status_code=200, json_content={'result': 'OK'})

    monkeypatch.setattr(requests, 'post', mock_post)
    got = transcriber.submit_for_recognition(
            audio_file_uri,
            api_key='hdtge'
       )
    assert got == {'result': 'OK'}

@pytest.fixture
def audio_file_uri():
    return 'gs://bucketName/object_name'

@dataclass
class _MockResponse:
    status_code: str
    json_content: dict

    def json(self):
        return self.json_content
