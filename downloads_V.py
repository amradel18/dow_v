import streamlit as st
import yt_dlp
import os
import time
from datetime import datetime

st.set_page_config(page_title="Video Downloader Log", page_icon="🎥")

st.title("🎥 Video Downloader with Download Button")

video_url = st.text_input("🎞️ Enter video URL:")
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

def download_video(url, referer_header, user_agent_header):
    try:
        output_path = 'downloads/%(title)s.%(ext)s'
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            'outtmpl': output_path,
            'quiet': True,
            'progress_hooks': [progress_hook],
            'http_headers': {
                'Referer': referer_header,
                'User-Agent': user_agent_header
            },
            'retries': 5,
            'ignoreerrors': True,
            'nooverwrites': True,
            'continuedl': True,
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info("⏳ Download started...")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        st.success("✅ Download completed successfully!")

        with open(filename, "rb") as f:
            st.download_button(
                label="🎬 Click to Download Video",
                data=f,
                file_name=os.path.basename(filename),
                mime="video/mp4"
            )

        os.remove(filename)

    except yt_dlp.utils.DownloadError as e:
        st.error(f"❌ Download error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

if st.button("⬇️ Start Download"):
    if not video_url:
        st.warning("⚠️ Please provide the video URL.")
    else:
        download_video(video_url, referer, user_agent)

st.caption(f"© {datetime.now().year} | Developed by YourName | Powered by yt-dlp")
