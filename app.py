from flask import Flask, render_template, request, redirect
import os
from moviepy.editor import VideoFileClip
import moviepy.editor as mp
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import openai  # Import OpenAI library

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set your OpenAI GPT-3 API key
openai.api_key = 'OpenAI GPT-3 API key'

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return redirect(request.url)

    video_file = request.files['video']

    if video_file.filename == '':
        return redirect(request.url)

    if video_file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_video.mp4')
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_audio.wav')
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_text.txt')

        video_file.save(video_path)

        # Video to Audio
        video_to_audio(video_path, audio_path)

        # Audio to Text
        text_result = audio_to_text(audio_path)

        # Save Text to File
        with open(text_path, "w") as text_file:
            text_file.write(text_result)

        # Get tags using GPT-3 API
        tags = get_tags_from_gpt3(text_result)

        return render_template('result.html', text_result=text_result, tags=tags)

def video_to_audio(input_video, output_audio):
    video_clip = VideoFileClip(input_video)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio)
    video_clip.close()

def audio_to_text(input_audio):
    recognizer = sr.Recognizer()

    with sr.AudioFile(input_audio) as audio_file:
        audio_clip = AudioFileClip(input_audio)
        audio_duration = audio_clip.duration

    chunk_duration = 60  # Specify the duration of each chunk in seconds

    # Calculate the number of chunks
    num_chunks = int(audio_duration / chunk_duration) + 1

    result_text_parts = []

    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = min((i + 1) * chunk_duration, audio_duration)

        with sr.AudioFile(input_audio) as audio_file:
            audio_data_chunk = recognizer.record(audio_file, duration=end_time - start_time, offset=start_time)

        try:
            text_part = recognizer.recognize_google(audio_data_chunk)
            result_text_parts.append(text_part)
        except sr.UnknownValueError:
            result_text_parts.append("Speech Recognition could not understand the audio")

    # Concatenate the recognized text parts
    final_text = ' '.join(result_text_parts)

    return final_text

def get_tags_from_gpt3(input_text):
    # Use GPT-3 to generate tags
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"give me tags for following text:\n\n{input_text}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )

    # Extract tags from the GPT-3 response and format them
    tags = [tag.strip() for tag in response["choices"][0]["text"].split("#") if tag.strip() and not tag.strip().isdigit()]

    # Ensure there are tags, otherwise return an empty list
    return tags if tags else None


if __name__ == '__main__':
    app.run(debug=True)
