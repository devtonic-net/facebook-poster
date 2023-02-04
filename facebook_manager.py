import os
import requests

class FacebookPoster:
    """Class for posting content to a Facebook page.

    Attributes:
        FACEBOOK_PAGE_ID (str): ID of the Facebook page.
        PAGE_ACCESS_TOKEN (str): Access token of the Facebook page.
        PHOTO_ENDPOINT (str): Endpoint URL for posting photos to the Facebook page.
        VIDEO_ENDPOINT (str): Endpoint URL for posting videos to the Facebook page.
        PAGE_FEED_ENDPOINT (str): Endpoint URL for posting to the Facebook page feed.
    """

    def __init__(self, page_id: str, access_token: str) -> None:
        """Inits FacebookPoster class with Facebook page ID and access token.

        Args:
            page_id (str): ID of the Facebook page.
            access_token (str): Access token of the Facebook page.
        """
        self.FACEBOOK_PAGE_ID = page_id
        self.PAGE_ACCESS_TOKEN = access_token
        self.PHOTO_ENDPOINT = f"https://graph.facebook.com/{self.FACEBOOK_PAGE_ID}/photos"
        self.VIDEO_ENDPOINT = f"https://graph-video.facebook.com/{self.FACEBOOK_PAGE_ID}/videos"
        self.PAGE_FEED_ENDPOINT = f"https://graph.facebook.com/{self.FACEBOOK_PAGE_ID}/feed"


    def upload_image(self, image_path: str, image_description: str = None):
        """
        Uploads an image to Facebook. The image will not be published on
        the page Feed, however it will be embeddable in posts via its id.

        Parameters:
            image_path (str): The path to the image to be uploaded or the URL of the image.
            image_description (str, optional): The description to be added to the image. Default is None.
        Returns:
            dict/None: The JSON response from the Facebook API or None if error.
        Raises:
            Exception: If there is an error uploading the image, the error message is printed.
        """
        params = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "message": image_description,
            "published": False
        }  
        if os.path.isfile(image_path):
            files = {"file": open(image_path, "rb")}
        else:
            # We presume the string to be an image URL
            files = None
            params["url"] = image_path
        try:
            response = requests.post(self.PHOTO_ENDPOINT, files=files, params=params)
        except Exception as e:
            print(f"Error uploading image to Facebook: {e}")
            return None           
        return response.json()

    
    def create_regular_post(self, post_text: str, image_paths: list = None, link: str = None):
        """
        Create a new Facebook post (text only; text and images; text and link). If both image_paths
        and link are declared, Facebook will ignore the uploaded images and will create a link post
        (the post will have text and an embedded featured image from the linked article).

        Parameters:
            post_text (str): The text to be posted on Facebook.
            image_paths (list of str, optional): A list of paths to images to be uploaded or URLs of images. Default is None.
            link (str, optional): The URL to be attached to the post. Default is None.  

        Returns:
            dict/None: The JSON response from the Facebook API or None if exception is raised.

        Raises:
            Exception: If there is an error creating the post, the error message is printed.
        """
        data = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "message": post_text,
        }
        # Since Facebook will ignore the images if link is present,
        # we check to see if we should skip uploading the files
        if image_paths and not link:
            image_ids = []
            for image_path in image_paths:
                uploaded_image = self.upload_image(image_path)
                if uploaded_image.get("id"):
                    image_ids.append(uploaded_image["id"])
            for index, image_id in enumerate(image_ids):
                data[f"attached_media[{index}]"] = f"{{'media_fbid': '{image_id}'}}"       
        if link:
            data["link"] = link
        try:
            response = requests.post(self.PAGE_FEED_ENDPOINT, data=data)
        except Exception as e:
            print(f"Error creating Facebook post: {e}")
        return response.json()

        
    def create_video_post(self, video_path: str, title: str = None, description: str = None):
        """
        Posts a video to a Facebook page and adds a title and a description to it.

        Parameters:
            video_path (str): Path to the video file.
            title (str, optional): The title to be added to the video post.
            description (str, optional): The description to be added to the video post.

        Returns:
            dict/None: JSON response from the Facebook Graph API with the ID of the newly posted video or None in case of error.
        """
        files = {
            "file": open (video_path, "rb")
        }
        params = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "title": title,
            "description": description,
        }
        try:
            response = requests.post(self.VIDEO_ENDPOINT, files=files, params=params)
        except Exception as e:
            print(f"Error creating Facebook post with video: {e}")
            return None
        return response.json()

