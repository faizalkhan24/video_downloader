from flask import Flask, render_template, request, jsonify
from pytube import YouTube, Playlist
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_path = os.path.join('downloads')  # Set the default download path

    try:
        if 'playlist' in url.lower():
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                download_video(video_url, output_path)
        else:
            download_video(url, output_path)

        return jsonify({'success': True, 'message': 'Download completed!'})

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return jsonify({'success': False, 'error_message': error_message})

def download_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    print("Downloading:", yt.title)
    download_path = os.path.join('static', 'videos')
    os.makedirs(download_path, exist_ok=True)
    file_path = os.path.join(download_path, f'{yt.title}.mp4')
    stream.download(output_path)
    os.rename(os.path.join(output_path, f'{yt.title}.mp4'), file_path)
    print("Download completed!")

if __name__ == "__main__":
    app.run(debug=True)
