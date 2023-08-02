import os.path
from uuid import uuid4
from pydub import AudioSegment
from mimetypes import guess_type
from typing import Generator
from moviepy.editor import VideoFileClip
import requests
import re
from dotenv import load_dotenv
import settings
load_dotenv()

openai_key = os.environ.get('OPENAI_API_KEY')


def transcribe_file(file_path):

    if is_audio(file_path):
        gen = transcribe_audio(file_path)
    elif is_video(file_path):
        gen = transcribe_video(file_path)
    else:
        return

    filename, _ = os.path.splitext(file_path)
    with open(f'{filename}.txt', 'w') as file:
        for text in gen:
            file.write(re.sub(r'([.?!])', r'\1\n ', text))


def get_type(filename):
    mime_type, _ = guess_type(filename)
    if mime_type is not None:
        return mime_type


def is_audio(file_path):
    file_type = get_type(file_path)
    return 'audio' in file_type if file_type is not None else None


def is_video(file_path):
    file_type = get_type(file_path)
    return 'video' in file_type if file_type is not None else None


def transcribe_audio(filename):
    audio = AudioSegment.from_file(filename)
    for chunk in chop_audio(audio, 120):
        text = transcribe_audio_segment(chunk)
        yield text


def transcribe_video(file_path):
    video = VideoFileClip(file_path)
    audio = video.audio
    filename = f'file/{uuid4()}.mp3'
    audio.write_audiofile(filename)
    for text in transcribe_audio(filename):
        yield text


def transcribe_audio_segment(audio: AudioSegment):
    whisper_url = 'https://api.openai.com/v1/audio/transcriptions'

    headers = {'Authorization': f'Bearer {openai_key}'}
    filename = f'file/{uuid4()}.mp3'
    audio.export(out_f=filename, format='mp3')
    with open(filename, 'rb') as file:
        os.remove(filename)
        payload = {
            'model': (None, 'whisper-1'),
            'file': ('file.mp3', file),
            'prompt': (None, settings.PROMPT),
            'response_format': (None, settings.RESPONSE_FORMAT),
            'language': (None, settings.LANGUAGE),
            'temperature': (None, settings.TEMPERATURE)

        }
        response = requests.post(url=whisper_url, files=payload, headers=headers)
    if response.status_code == 401:
        print('Unauthorized')
    elif response.status_code == 400:
        print(response.content)
    elif response.status_code == 200:
        return response.json()['text']


def chop_audio(audio: AudioSegment, chunk_duration: int) -> Generator:
    """
    :param audio: Audiosegment
    :param chunk_duration: chunk duration in seconds
    add bytes in input
    """

    start_time = 0
    end_time = chunk_duration * 1000

    while True:
        if start_time >= audio.duration_seconds * 1000:
            break

        yield audio[start_time:end_time]

        start_time = end_time
        end_time += chunk_duration * 1000
