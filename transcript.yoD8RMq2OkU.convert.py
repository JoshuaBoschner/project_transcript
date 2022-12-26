# import youtube transcript api
# https://pypi.org/project/youtube-transcript-api/
from typing import Text
from youtube_transcript_api import YouTubeTranscriptApi
# the base class to inherit from when creating your own formatter.
# some provided subclasses, each outputs a different string format.
from youtube_transcript_api.formatters import Formatter
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import WebVTTFormatter

import time
import os
import re

from textblob import TextBlob

original_file = "test.txt"
output_file = "temp.txt"
output_path = os.getcwd()

def simple_line_reader():
    with open(original_file, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != "line you want to remove...":
                f.write(i)
        f.truncate()


def simple_string_deleter():
    string_to_delete = ['Emma', 'Kelly']
    with open(original_file, "r") as input:
        with open(output_file, "w") as output:
            for line in input:
                for word in string_to_delete:
                    line = line.replace(word, "")
                output.write(line)
    # replace file with original name
    # os.remove(original_file)


def get_videoId_from_filename():
    filename = os.path.basename(__file__)
    m = re.search('transcript.(.+?).convert', filename)
    if m:
        video_id = m.group(1)
    return video_id

def correct_sentence_spelling(sentence):
    sentence = TextBlob(sentence)
    result = sentence.correct()
    print(result)

video_id = get_videoId_from_filename()
transcript = YouTubeTranscriptApi.get_transcript(
    video_id, languages=['de', 'en'])

text_formatter = TextFormatter()
json_formatter = JSONFormatter()

# .format_transcript(transcript) turns the transcript into a Text string.
text_formatted = text_formatter.format_transcript(transcript).replace("\n", " ").replace("[Music]", "")
# .format_transcript(transcript) turns the transcript into a JSON string.
json_formatted = json_formatter.format_transcript(transcript)

#text_formatted = correct_sentence_spelling(text_formatted)
print(f'File output to: {output_path}+transcript.{video_id}.txt')

# Now we can write it out to a text file.
with open(os.path.join(output_path, f'transcript.{video_id}.txt'), 'w', encoding='utf-8') as text_file:
    text_file.write(text_formatted)
# Now we can write it out to a json file.
#with open(os.path.join(output_path, f'transcript.{video_id}.json'), 'w', encoding='utf-8') as json_file:
#    json_file.write(json_formatted)

