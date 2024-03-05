from pytube import YouTube

def download_video(url, output_path):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Download the video
        print("Downloading:", yt.title)
        stream.download(output_path)
        print("Download completed!")

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    video_url = input("Enter the URL of the video: ")
    output_path = input("Enter the output path to save the video: ")

    download_video(video_url, output_path)
