import streamlit as st
import yt_dlp
import os
import glob
import time
from datetime import datetime

st.set_page_config(page_title="Video Downloader", page_icon="🎥")

st.title("🎥 Video Downloader")

video_url = st.text_input("🎞️ Enter video URL:")
referer = "https://google.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

log_placeholder = st.empty()

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '0')
        eta = d.get('_eta_str', '00:00')
        log_placeholder.text(f"[download] {percent} at {speed} ETA {eta}")
    elif d['status'] == 'finished':
        log_placeholder.text("✅ Download completed successfully!")

def download_video(url, referer_header, user_agent_header):
    try:
        os.makedirs("downloads", exist_ok=True)
        output_template = "downloads/video_download.%(ext)s"

        ydl_opts = {
            'outtmpl': output_template,
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
            'format': 'best[ext=mp4]/best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info("⏳ Download started...")
            ydl.download([url])

        # get downloaded file
        downloaded_files = glob.glob("downloads/video_download.*")
        if downloaded_files:
            video_file = downloaded_files[0]
            with open(video_file, "rb") as f:
                st.download_button(
                    label="🎬 Click to Download Video",
                    data=f,
                    file_name=os.path.basename(video_file),
                    mime="video/mp4"
                )
            os.remove(video_file)
        else:
            st.error("❌ No video file found after download.")

    except yt_dlp.utils.DownloadError as e:
        st.error(f"❌ Download error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

if st.button("⬇️ Start Download"):
    if not video_url:
        st.warning("⚠️ Please enter a video URL.")
    else:
        download_video(video_url, referer, user_agent)

st.caption(f"© {datetime.now().year} | Developed by YourName | Powered by yt-dlp")
