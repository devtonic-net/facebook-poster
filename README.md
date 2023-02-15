# Facebook Poster

FacebookPoster is a Python class that allows you to post content to a Facebook page. This class is suitable for automating social media posts.

## Usage

#### 1. Store your Facebook credentials safely
In your project folder, create a ```.env``` file and enter your Facebook page ID and access token, like this:
```
FACEBOOK_PAGE_ID = '1234567890' # replace with your own page ID
PAGE_ACCESS_TOKEN = 'ABCDEFGHI' # replace with your own page access token
```
#### 2. Load the credentials and create an instance of the class
In ```main.py```, load the Facebook credentials and create an instance of the FacebookPoster class. Once you have an instance, you can use its methods to post content to the Facebook page. Use the following code:

```
import os
from facebook_manager import FacebookPoster
from dotenv import load_dotenv
load_dotenv()

poster = FacebookPoster(os.getenv("FACEBOOK_PAGE_ID"), os.getenv("PAGE_ACCESS_TOKEN")
```
### 📷  |  Posting text and still images to Facebook

To create a post with text and one or more images, use the ```create_image_post``` method. You can specify the text of the post and the paths to one or more images that you want to upload, or one or more URIs, if the images are hosted online. Here's an example:

Use with images saved on your computer:
```
poster.create_image_post("Post with mixed images!", ["path/to/local_img.jpg", "https://site.com/online_img.jpg"])
```

### 🎥  |  Posting text and video to Facebook

To create a video post on a Facebook page, use the ```create_video_post``` method. You can specify the path to the video file, as well as an optional title and description. Here's an example:

```
poster.create_video_post("path/to/video.mp4", "My cool video title", "Description of the video")
```
### 🔗  |  Posting text and links to Facebook

To post text to Facebook, use the ```create_text_post``` method. You can specify the text of the post, as well as an optional link to include in the post. Here's an example:

```
poster.create_text_post("Check out my blog post about Python!", "https://example.com/blog/python")
```

## Requirements

The FacebookPoster class requires the following packages:

    python-dotenv
    requests

### License

FacebookPoster is licensed under the MIT License.
