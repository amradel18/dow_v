import streamlit as st
from urllib.parse import urlparse

# إعداد الصفحة
st.set_page_config(page_title="🎥 Video Downloader", page_icon="🎥")

# عنوان التطبيق
st.title("🎥 Direct Video Downloader")

# حقل إدخال رابط الفيديو
video_url = st.text_input("🎞️ Enter video URL:")

# زر تنفيذ
if st.button("Generate Download Link"):
    if not video_url:
        st.warning("⚠️ Please enter a video URL.")
    else:
        # التحقق من امتداد الرابط
        parsed_url = urlparse(video_url)
        if parsed_url.path.endswith(".mp4"):
            # لو الرابط مباشر (mp4)
            st.success("✅ This is a direct video link.")
            st.markdown(f"""
                <a href="{video_url}" download target="_blank">
                📥 <button style='padding:10px 20px; font-size:16px; background-color:#4CAF50; color:white; border:none; border-radius:5px;'>Download Video</button>
                </a>
            """, unsafe_allow_html=True)
        else:
            # لو الرابط مش مباشر (زي YouTube)
            st.error("⚠️ This link is not a direct video link (e.g. YouTube or protected stream).")
            st.write("💡 If it's a YouTube video, you can download it on your computer using this command:")
            st.code(f'yt-dlp "{video_url}"', language='bash')

# التوقيع
st.caption("© 2025 | Developed by YourName | Powered by Streamlit")
