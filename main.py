import os
from facebook_manager import FacebookPoster
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
fb = FacebookPoster(FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN)
# video = fb.create_video_post("crows.mp4")
# print(video)
foto = fb.create_regular_post("O noua postare", ["caini.jpg"])
print(foto)