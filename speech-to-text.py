#! /usr/bin/env python
import os
import pathlib
import json

import click

@click.group()
def cli():
    pass

@cli.command(name='mp3-to-wav')
@click.argument('mp3-file-path')
def mp3_to_wav(mp3_file_path):
    import mp3_to_wav
    mp3_to_wav.mp3_to_wav(mp3_file_path)

@cli.command(name='upload-audio')
@click.argument('audio-file-path')
@click.argument('bucket-name')
def cloud_upload(audio_file_path, bucket_name):
    import cloud_store
    cloud_store.upload_audio_file_to_bucket(audio_file_path, bucket_name)

@cli.command(name='transcribe-audio')
@click.argument('audio-file-uri')
def transcribe_audio(audio_file_uri):
    import recognizer
    response = recognizer.submit_for_recognition(audio_file_uri, os.environ['API_KEY'])
    with open(f'{pathlib.Path(audio_file_uri).name}.json', 'w') as f:
        json.dump(response, f)
    print(f'OperationName: {response.name}')
    print('\nOperation metadata persisted to disk at:{pathlib.Path(audio_file_uri).name}.json')



@cli.command(name='transcription-status')
@click.argument('operation-name')
@click.option('--write-to-file', is_flag=True, help='write transcript to file instead of srdout')
def transcription_status(operation_name, write_to_file):
    import recognizer
    status = recognizer.recognition_request_status(operation_name)
    print(f'OperationName: {status.operation_name}')
    print(f'ProgressPercent: {status.progress_percent}')
    print(f'StartTime: {status.progress_percent}')
    print(f'LastUpdated: {status.last_update_time}')
    print('\nTRANSCRIPT\n')
    if write_to_file and status.progress_percent == 100:
        with open(f'{status.operation_name}.transcript', 'w') as f:
            f.write(status.transcript)
        print(f'Transcript written to file:{status.operation_name}.transcript')

    else:
        print(status.transcript)

if __name__ == '__main__':
    cli()
