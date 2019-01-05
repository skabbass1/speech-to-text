from dataclasses import dataclass

import pytest
from dateutil.parser import parse
import recognizer

def test_build_request_payload(audio_file_uri):
    """
    it correctly builds the request payload
    """
    got = recognizer._build_request_payload(audio_file_uri)
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
    import auth

    def mock_post(uri, json, headers):
        return _MockResponse(status_code=200, json_content={'result': 'OK'})

    monkeypatch.setattr(requests, 'post', mock_post)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: 'token')

    got = recognizer.submit_for_recognition(
            audio_file_uri,
            api_key='hdtge'
       )
    assert got == {'result': 'OK'}

def test_submit_for_recognition_raises(audio_file_uri, monkeypatch):
    """
    it raises `RecognizerException` on non 200 response code from
    Google speech API`
    """
    import requests
    import auth

    def mock_post(uri, json, headers):
        return _MockResponse(status_code=400, json_content={'error': 'boom!'})

    monkeypatch.setattr(requests, 'post', mock_post)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: 'token')

    with pytest.raises(recognizer.RecognizerException):
        got = recognizer.submit_for_recognition(
                audio_file_uri,
                api_key='hdtge'
           )

def test_recognition_request_status_raises(monkeypatch):
    """
    it raises `RecognizerException` on non 200 response code from
    Google speech API`
    """
    import requests
    import auth

    def mock_get(uri, headers):
        return _MockResponse(status_code=400, json_content={'error': 'boom!'})

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: 'token')
    with pytest.raises(recognizer.RecognizerException):
        got = recognizer.recognition_request_status(operation_name=1837354543)

def test_recognition_request_status(monkeypatch):
    """
    given a completed transcription operation
    it returns recognizer.RecognitionResults object correctly populated
    """

    import requests
    import auth

    def mock_get(uri, headers):
        return _MockResponse(
                status_code=200,
                json_content={
                    'name': 1837354543,
                    'metadata': {
                        'progressPercent': 100,
                        'startTime': '2019-01-03T13:41:37.522968Z',
                        'lastUpdateTime': '2019-01-03T13:41:37.522968Z',
                        },
                    'response':{
                        'results':[
                            {'alternatives': [{'transcript': 'hello world', 'confidence': 0.98226684}]},
                            {'alternatives': [{'transcript': 'hello back', 'confidence': 0.98226684}]},
                            ]
                        },
                    }
                )

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: 'token')

    got = recognizer.recognition_request_status(operation_name=1837354543)
    assert got.operation_name == 1837354543
    assert got.progress_percent == 100
    assert got.start_time == parse('2019-01-03T13:41:37.522968Z')
    assert got.last_update_time == parse('2019-01-03T13:41:37.522968Z')
    assert got.transcript == 'Hello world. Hello back'

def test_recognition_request_status_inprogress(monkeypatch):
    """
    given an in propgress transcription operation
    it returns recognizer.RecognitionResults object correctly populated
    """

    import requests
    import auth

    def mock_get(uri, headers):
        return _MockResponse(
                status_code=200,
                json_content={
                    'name': 1837354543,
                    'metadata': {
                        'progressPercent': 100,
                        'startTime': '2019-01-03T13:41:37.522968Z',
                        'lastUpdateTime': '2019-01-03T13:41:37.522968Z',
                        },
                    }
                )

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(auth, 'get_auth_token', lambda: 'token')

    got = recognizer.recognition_request_status(operation_name=1837354543)
    assert got.operation_name == 1837354543
    assert got.progress_percent == 100
    assert got.start_time == parse('2019-01-03T13:41:37.522968Z')
    assert got.last_update_time == parse('2019-01-03T13:41:37.522968Z')
    assert got.transcript == None


@pytest.fixture
def audio_file_uri():
    return 'gs://bucketName/object_name'

@dataclass
class _MockResponse:
    status_code: str
    json_content: dict

    def json(self):
        return self.json_content
