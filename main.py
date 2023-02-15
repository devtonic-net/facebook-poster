import os
from facebook_manager import FacebookPoster
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
fb = FacebookPoster(FACEBOOK_PAGE_ID, PAGE_ACCESS_TOKEN)

text_post = fb.create_text_post("Text post with link", "https://example.com/")
print(text_post)

text_post_local_images = fb.create_image_post(
    "Text post with local images", ["path_to_image1.jpg", "path_to_image2.jpg"])
print(text_post_local_images)

text_post_url_images = fb.create_image_post("Text post with remote images", [
                                            "https://images.com/a.jpg", "https://images.com/b.jpg"])
print(text_post_url_images)

video_post = fb.create_video_post(
    "path_to_video.mp4", "Video title", "Video description", )
print(video_post)
