import os
import re
import asyncio
import subprocess
from urllib.parse import urlparse, parse_qs
import yt_dlp
import requests
from config import COOKIES_PATH, DENO_BIN, FFMPEG_PATH
def clean_url(raw_url: str) -> str:
    url = raw_url.strip()
    shorts_match = re.search(r'(?:youtube\.com|youtu\.be)/shorts/([a-zA-Z0-9_-]+)', url)
    if shorts_match:
        return f"https://www.youtube.com/watch?v={shorts_match.group(1)}"
    youtu_be_match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if youtu_be_match:
        return f"https://www.youtube.com/watch?v={youtu_be_match.group(1)}"
    if "youtube.com/watch" in url:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        v = query.get("v")
        if v:
            return f"https://www.youtube.com/watch?v={v[0]}"
    return url
def get_ytdlp_options(output_template: str, client_type: str = "web"):
    opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'concurrent_fragment_downloads': 5,
        'outtmpl': output_template,
        'writethumbnail': True,
        'format': (
            'best[filesize<48M]/'
            'bestvideo[filesize<42M]+bestaudio[filesize<6M]/'
            'bestvideo[height<=720]+bestaudio/'
            'best[height<=720]/'
            'best'
        ),
        'merge_output_format': 'mp4',
        'js_runtimes': {'deno': {'path': DENO_BIN}},
        'remote_components': ['ejs:github'],
    }
    if client_type == "android":
        opts['extractor_args'] = {'youtube': {'player_client': ['android', 'ios']}}
    elif client_type == "tv":
        opts['extractor_args'] = {'youtube': {'player_client': ['tv_embedded', 'web_embedded']}}
    if os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 10:
        opts['cookiefile'] = COOKIES_PATH
    return opts
def run_ytdlp_download(url: str, output_template: str):
    for client in ["web", "android", "tv"]:
        try:
            with yt_dlp.YoutubeDL(get_ytdlp_options(output_template, client)) as ydl:
                ydl.download([url])
                return
        except Exception as e:
            print(f"Downloader client '{client}' failed, trying next: {e}")
            continue
    with yt_dlp.YoutubeDL(get_ytdlp_options(output_template, "web")) as ydl:
        ydl.download([url])
def find_downloaded_files(prefix: str):
    video_file = None
    thumb_file = None
    for f in os.listdir('.'):
        if f.startswith(prefix) and not f.endswith(('.part', '.ytdl', '.temp')):
            if re.search(r'\.f\d+\.', f):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                thumb_file = f
            elif ext in ['.mp4', '.mkv', '.webm', '.mov', '.avi']:
                if os.path.getsize(f) > 50 * 1024:
                    video_file = f
    return video_file, thumb_file
async def compress_video_if_needed(video_path: str, prefix: str) -> str:
    file_size = os.path.getsize(video_path)
    if file_size <= 49 * 1024 * 1024:
        return video_path
    print(f"File size {file_size / (1024*1024):.2f}MB exceeds 49MB. Auto-compressing with FFmpeg...")
    compressed_video = f"{prefix}_comp.mp4"
    compress_cmd = [
        FFMPEG_PATH, "-y",
        "-i", video_path,
        "-vf", "scale=-2:480",
        "-c:v", "libx264",
        "-crf", "28",
        "-preset", "faster",
        "-c:a", "aac",
        "-b:a", "96k",
        "-movflags", "+faststart",
        compressed_video
    ]
    await asyncio.to_thread(subprocess.run, compress_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(compressed_video) and os.path.getsize(compressed_video) > 1000:
        return compressed_video
    return video_path
async def extract_audio_from_video(video_path: str, output_path: str) -> bool:
    cmd = [FFMPEG_PATH, "-y", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-q:a", "2", output_path]
    await asyncio.to_thread(subprocess.run, cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
async def convert_thumbnail_to_jpg(thumb_path: str, output_path: str) -> bool:
    await asyncio.to_thread(
        subprocess.run,
        [FFMPEG_PATH, "-y", "-i", thumb_path, output_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
def fetch_pinterest_direct_image(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10)
        img_matches = re.findall(r'https://i\.pinimg\.com/(?:originals|736x)/[^\s"\'\>]+\.(?:jpg|png|jpeg|webp)', res.text)
        if img_matches:
            return img_matches[0]
    except Exception:
        pass
    return None
