# === CODE INDEX ===
# Legacy Brightcove Download Script       Line 6

import yt_dlp


ydl_opts = {
    'format': 'best',
    'outtmpl': 'brightcove_video.mp4',
}

video_url = 'https://players.brightcove.net/3887645559001/I5U1azlXZ_default/index.html?videoId=5978804382001'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
