import streamlit as st
import yt_dlp
import os
import time
from datetime import datetime

st.set_page_config(page_title="Video Downloader Log", page_icon="🎥")

st.title("🎥 Video Downloader with Detailed Log Line")

video_url = st.text_input("🎞️ Enter video URL:")
download_path = st.text_input("📁 Download path:", value="C:/Videos/")
referer = "https://google.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

log_placeholder = st.empty()

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        elapsed = d.get('elapsed', 0)
        speed = d.get('speed', 0)

        percent = (downloaded_bytes / total_bytes * 100) if total_bytes else 0
        downloaded_mb = downloaded_bytes / 1024 / 1024
        total_mb = total_bytes / 1024 / 1024 if total_bytes else 0
        speed_mb = speed / 1024 / 1024 if speed else 0
        elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed))

        if total_bytes:
            log_line = f"[download] {percent:.1f}% of {total_mb:.2f}MiB in {elapsed_time} at {speed_mb:.2f}MiB/s"
        else:
            log_line = f"[download] {downloaded_mb:.2f}MiB downloaded (total size unknown)"

        log_placeholder.text(log_line)

    elif d['status'] == 'finished':
        log_placeholder.text("✅ Download completed successfully!")

def download_video(url, path, referer_header, user_agent_header):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s_%(id)s.%(ext)s'),
            'quiet': True,
            'progress_hooks': [progress_hook],
            'http_headers': {
                'Referer': referer_header,
                'User-Agent': user_agent_header
            },
            'retries': 5,
            'ignoreerrors': True,
            'nooverwrites': True,
            'continuedl': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info("⏳ Download started...")
            ydl.download([url])
            st.success("✅ Download completed successfully!")

    except yt_dlp.utils.DownloadError as e:
        st.error(f"❌ Download error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

if st.button("⬇️ Start Download"):
    if not video_url or not download_path:
        st.warning("⚠️ Please provide both the video URL and download path.")
    else:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        download_video(video_url, download_path, referer, user_agent)

st.caption(f"© {datetime.now().year} | Developed by YourName | Powered by yt-dlp")
