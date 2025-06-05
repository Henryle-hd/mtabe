import yt_dlp
import os
import tempfile
import time
import glob
from mtabe.config.config import reusable_panel_console

def get_youtube_subtitles(url: str, lang: str = "en") -> str:
    """
    Download subtitles from a YouTube video using yt_dlp.

    Args:
        url (str): The URL of the YouTube video.
        lang (str): Language code for subtitles (default: 'en').

    Returns:
        str: The subtitles as a plain string.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [lang],
            'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(tempdir, '%(id)s.%(ext)s'),
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'requested_subtitles' not in info or lang not in info['requested_subtitles']:
                    raise ValueError(f"No subtitles found for language '{lang}' in this video.")
                ydl.download([url])
        except Exception as e:
            return f"Failed to download subtitles: {e}"

        # Wait briefly for filesystem to catch up
        time.sleep(0.5)

        # Find .vtt files in the temp directory
        vtt_files = glob.glob(os.path.join(tempdir, '*.vtt'))
        if not vtt_files:
            return "No subtitle file was created."

        # Take the first one (or you could match exact language suffix)
        subtitle_file = vtt_files[0]

        try:
            with open(subtitle_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            subtitle_text = []
            for line in lines:
                if line.strip() == "" or "-->" in line or line.startswith("WEBVTT"):
                    continue
                subtitle_text.append(line.strip())

            return "\n".join(subtitle_text)
        except Exception as e:
            reusable_panel_console(text=f"Failed to read subtitle file\nFrom [italic blue]{url}[/italic blue],\nError:{e}",border_style='red',text_style='red', title='Oops❌')
            quit()


if __name__ == "__main__":
    print(get_youtube_subtitles("https://youtu.be/lnMMyHa9Y-Q"))