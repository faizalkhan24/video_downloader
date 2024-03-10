from flask import Flask, render_template, request, jsonify
from pytube import YouTube, Playlist
import os
import re
from pytube.cli import on_progress
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Auto-reload templates for development
app.config['BOOTSTRAP_SERVE_LOCAL'] = True  # Use locally installed Bootstrap library

from flask_bootstrap import Bootstrap
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_path = os.path.join('downloads')  # Set the default download path
    download_path = os.path.join('static', 'videos')  # Set the download path for the final videos

    # Create the necessary directories
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(download_path, exist_ok=True)

    try:
        if 'playlist' in url.lower():
            playlist = Playlist(url)
            download_playlist(playlist, output_path, download_path)
        else:
            download_video(url, output_path, download_path)

        return jsonify({'success': True, 'message': 'Download completed!'})

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return jsonify({'success': False, 'error_message': error_message})

    # Ensure a valid response is returned in all cases
    return jsonify({'success': False, 'error_message': 'Unknown error occurred.'})

def download_playlist(playlist, output_path, download_path):
    for video_url in playlist.video_urls:
        download_video(video_url, output_path, download_path)

def download_video(url, output_path, download_path):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.get_highest_resolution()
    print("Downloading:", yt.title)

    # Replace invalid characters with underscores
    cleaned_title = re.sub(r'[\/:*?"<>|]', '_', yt.title)

    # Use the download path for the final file path
    file_name = f'{cleaned_title}.mp4'
    file_path_final = os.path.join(download_path, file_name)

    start_time = time.time()

    try:
        stream.download(download_path)
        elapsed_time = time.time() - start_time
        download_speed = stream.filesize / elapsed_time / (1024 * 1024)  # Convert to MB/s
        print(f"\nDownload completed! Download Speed: {download_speed:.2f} MB/s")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Download failed!")

if __name__ == "__main__":
    app.run(debug=True)
