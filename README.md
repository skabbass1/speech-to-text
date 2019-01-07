# Task Description
You have been hired by a small company which does audio recordings of speeches given at conferences and events. The company wants to expand it offerrings to customers by providing a transcript of the recorded speech alongside the audio. Your task is to write an application which makes this possible. Specifically, your application needs to provide the following functionality:

1. Convert an MP3 file to a WAV file which could later be used for audio editing or for transciption. Note that the MP3 files are typically larger than 5MB
2. Use a third party transcription service such as Google Cloud Speech to Text to perform the transcription.
3. Expose a CLI as well as an API which could be used to submit a trasncription request and check on its status. Note that many third party speech to text APIS perform transcriptions asynchronously for larger audio files. Your application must be able to handle and asynchronous transcription request response cycle
4. The application should provide robust error handling and must include automated tests.

You can use the  the sample audio file in the `data` directory of this repo to test your application.
