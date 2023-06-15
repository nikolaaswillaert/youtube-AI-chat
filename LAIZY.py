from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

import os

video_id = input("Youtube link to transscribe: ")
video_id = video_id.split('=')[1]

full_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
formatter = TextFormatter()
full_text_formatted = formatter.format_transcript(full_text)

file_name = f"{video_id}.txt"

with open(file_name, 'w') as file:
    for i in full_text:
        file.write(i['text'] + " ")

print(f"File '{file_name}.txt' created and saved.")

