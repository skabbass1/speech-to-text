import http
import datetime
import dataclasses
import typing

import requests
from dateutil.parser import parse

import auth

_LONG_RUNNING_RECOGNIZE_URI = 'https://speech.googleapis.com/v1/speech:longrunningrecognize'
_RECOGNIZE_STATUS_URI = 'https://speech.googleapis.com/v1/operations/{operation_name}'


class RecognizerException(Exception):
    pass

@dataclasses.dataclass(frozen=True)
class RecognitionResults:
    operation_name: int
    progress_percent: int
    start_time: datetime
    last_update_time: datetime
    transcript: typing.Any

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
    data = response.json()
    return RecognitionResults(
               data['name'],
               data['metadata']['progressPercent'],
               parse(data['metadata']['startTime']),
               parse(data['metadata']['lastUpdateTime']),
               _transcript_from_response(data.get('response'))
            )

def _build_request_payload(uri):
    return {**_recognition_config(), **_recognition_audio(uri)}


def _recognition_config():
    return {'config': {'languageCode': 'en-US'}}

def _recognition_audio(uri):
    return {'audio':{'uri': uri}}

def _transcript_from_response(response):
    if response is None:
        return None
    return '. '.join((r['alternatives'][0]['transcript'].strip().capitalize() for r in response['results']))

