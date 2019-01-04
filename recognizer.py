import http

import requests

import auth

_LONG_RUNNING_RECOGNIZE_URI = 'https://speech.googleapis.com/v1/speech:longrunningrecognize'
_RECOGNIZE_STATUS_URI = 'https://speech.googleapis.com/v1/operations/{operation_name}'


class RecognizerException(Exception):
    pass

def submit_for_recognition(audio_file_uri, api_key):
    auth_token = auth.get_auth_token()
    response = requests.post(
            _LONG_RUNNING_RECOGNIZE_URI,
            json=_build_request_payload(audio_file_uri),
            headers={'Authorization': 'Bearer ' + auth_token}
    )

    if response.status_code != http.HTTPStatus.OK:
        raise RecognizerException(response.json()['error'])
    return response.json()

def recognition_request_status(operation_name):
    auth_token = auth.get_auth_token()
    response = requests.get(
            _RECOGNIZE_STATUS_URI.format(operation_name=operation_name),
            headers={'Authorization': 'Bearer ' + auth_token}
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
