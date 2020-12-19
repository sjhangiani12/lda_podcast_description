from __future__ import print_function
import time
import datetime
import boto3
import json
import requests
import os

BUCKET_NAME = "podcast-uw-final"
ACCESS_KEY_ID = os.environ['S3_KEY']
ACCESS_SECRET_KEY = os.environ['S3_SECRET']

def makeTranscript(job_name, audio_file, audio_type):
    # Create Boto Client for AWS
    transcribe = boto3.client('transcribe',
                    aws_access_key_id=ACCESS_KEY_ID,
                    aws_secret_access_key=ACCESS_SECRET_KEY,
                    region_name='us-east-2',)
    job_name = job_name
    job_uri = audio_file

    # Make Call to AWS
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=audio_type,
        LanguageCode='en-US'
    )

    # Poll for Status until completion (Success or Failure)
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Transcribing")
        time.sleep(5)

    # Print Output
    url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

    r = requests.get(url, allow_redirects=True)
    open('temp.json', 'wb').write(r.content)

    f = open('temp.json', "r")
    temp = f.read()

    script = json.loads(temp)['results']['transcripts'][0]['transcript']
    return script


# print(makeTranscript(job_name,"https://podcast-uw-final.s3.us-east-2.amazonaws.com/PodcastTestAudio/ObamaSports.mp3",'mp3'))