import http

import requests

_LONG_RUNNING_RECOGNIZE_URI = 'https://speech.googleapis.com/v1/speech:longrunningrecognize'

class RecognizerException(Exception):
    pass

def submit_for_recognition(audio_file_uri, api_key):
    response = requests.post(
            _LONG_RUNNING_RECOGNIZE_URI,
            json=_build_request_payload(audio_file_uri),
            params={'key': api_key}
    )

    if response.status_code != http.HTTPStatus.OK:
        raise RecognizerException(response.json()['error'])
    return response.json()


def _build_request_payload(uri):
    return {**_recognition_config(), **_recognition_audio(uri)}


def _recognition_config():
    return {'config': {'languageCode': 'en-US'}}

def _recognition_audio(uri):
    return {'audio':{'uri': uri}}
