from pytube import YouTube
from sys import argv
from tqdm import tqdm


def check_valid_youtube_link(link):
    try:
        yt = YouTube(link)
        return True
    except:
        return False


def show_available_qualities(yt):
    print("Available Qualities:")
    for stream in yt.streams:
        if "video" in str(stream) and "mp4" in str(stream):
            print(f"{stream.resolution} - {stream.mime_type}")


def is_valid_resolution(yt, resolution):
    for stream in yt.streams:
        if stream.resolution == resolution:
            return True
    return False


def download_video(link, resolution=None, custom_filename=None):
    yt = YouTube(link)

    if resolution:
        if not is_valid_resolution(yt, resolution):
            print("Invalid resolution.")
            return
        yd = yt.streams.filter(res=resolution, file_extension='mp4').first()
    else:
        yd = yt.streams.get_highest_resolution()

    if yd:
        print("Downloading...")
        if custom_filename:
            yd.download(output_path='.', filename=custom_filename)
        else:
            yd.download()
        print("Download completed successfully!")
    else:
        print("No video with the specified resolution is available.")


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python download_video.py <youtube_link1> <youtube_link2> ...")
    else:
        for link in argv[1:]:
            if not check_valid_youtube_link(link):
                print(f"Invalid YouTube link: {link}")
            else:
                yt = YouTube(link)
                print("Title: ", yt.title)
                print("View: ", yt.views)

                show_available_qualities(yt)

                resolution_choice = input(
                    "Choose a resolution (e.g., 720p, 1080p), or press Enter for the highest resolution: ")

                custom_filename = input("Enter a custom filename (or press Enter to use the default filename): ")

                if resolution_choice.strip():
                    download_video(link, resolution=resolution_choice, custom_filename=custom_filename)
                else:
                    download_video(link, custom_filename=custom_filename)