import os
import requests


class FacebookPoster:
    """A class for posting content to a Facebook page.

    Attributes:
        FACEBOOK_PAGE_ID (str): The ID of the Facebook page.
        PAGE_ACCESS_TOKEN (str): The access token of the Facebook page.
        PHOTO_ENDPOINT (str): The endpoint URL for posting photos to the Facebook page.
        VIDEO_ENDPOINT (str): The endpoint URL for posting videos to the Facebook page.
        PAGE_FEED_ENDPOINT (str): The endpoint URL for posting to the Facebook page feed.
    """
    FACEBOOK_PAGE_ID: str
    PAGE_ACCESS_TOKEN: str
    PHOTO_ENDPOINT: str
    VIDEO_ENDPOINT: str
    PAGE_FEED_ENDPOINT: str

    def __init__(self, page_id: str, access_token: str) -> None:
        """Initializes a FacebookPoster object with the ID of the Facebook page and its access token.

        Args:
            page_id (str): The ID of the Facebook page.
            access_token (str): The access token of the Facebook page.
        """
        self.FACEBOOK_PAGE_ID = page_id
        self.PAGE_ACCESS_TOKEN = access_token
        self.PHOTO_ENDPOINT = f"https://graph.facebook.com/{self.FACEBOOK_PAGE_ID}/photos"
        self.VIDEO_ENDPOINT = f"https://graph-video.facebook.com/{self.FACEBOOK_PAGE_ID}/videos"
        self.PAGE_FEED_ENDPOINT = f"https://graph.facebook.com/{self.FACEBOOK_PAGE_ID}/feed"

    def __upload_image(self, image_path: str, image_description: str = None) -> dict:
        """Uploads an image to Facebook. The image will not be published
        on the page feed, but it will be embeddable in posts via its ID.

        Args:
            image_path (str): The path to the image to be uploaded or the URL of the image.
            image_description (str, optional): The description to be added to the image. Defaults to None.

        Returns:
            dict: The JSON response from the Facebook API.

        Raises:
            Exception: If there is an error uploading the image, the error message is printed.
        """
        data = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "message": image_description,
            "published": False
        }
        if os.path.isfile(image_path):
            files = {"file": open(image_path, "rb")}
        else:
            # We presume the string to be an image URL
            files = None
            data["url"] = image_path
        try:
            response = requests.post(
                self.PHOTO_ENDPOINT, files=files, data=data)
            response.raise_for_status()
        except Exception as e:
            print(f"Error uploading image to Facebook: {e}")
            return None
        return response.json()

    def create_image_post(self, post_text: str, image_paths: list) -> dict:
        """
        Creates a post with text and image(s) on the Facebook page. 

        Parameters:
            post_text (str): The text to be posted on Facebook.
            image_paths (list of str): A list of paths to images to be uploaded or URLs of images.

        Returns:
            dict or None: The JSON response from the Facebook API or None if exception is raised.

        Raises:
            Exception: If there is an error creating the post, the error message is printed.
        """
        data = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "message": post_text,
        }
        image_ids = []
        for image_path in image_paths:
            uploaded_image = self.__upload_image(image_path)
            if uploaded_image.get("id"):
                image_ids.append(uploaded_image["id"])
        if image_ids:
            for index, image_id in enumerate(image_ids):
                data[f"attached_media[{index}]"] = f"{{'media_fbid': '{image_id}'}}"
        try:
            response = requests.post(self.PAGE_FEED_ENDPOINT, data=data)
        except Exception as e:
            print(f"Error creating Facebook post with image(s): {e}")
        return response.json()

    def create_video_post(self, video_path: str, title: str = None, description: str = None) -> dict:
        """
        Creates a video post with a title and a description on the Facebook page.

        Parameters:
            video_path (str): Path to the video file.
            title (str, optional): The title to be added to the video post.
            description (str, optional): The description to be added to the video post.

        Returns:
            dict or None: JSON response from the Facebook Graph API with the ID of the newly posted video or None in case of error.

        Raises:
            Exception: If there is an error creating the post, the error message is printed.
        """
        files = {
            "file": open(video_path, "rb")
        }
        data = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "title": title,
            "description": description,
        }
        try:
            response = requests.post(
                self.VIDEO_ENDPOINT, files=files, data=data)
        except Exception as e:
            print(f"Error creating Facebook post with video: {e}")
            return None
        return response.json()

    def create_text_post(self, text: str, url: str = None) -> dict:
        """
        Creates a text post on the Facebook page. 

        If a URL is provided, the post will include the link and an image
        that Facebook will try to extract from the linked resource.

        Args:
            text (str): The text content of the post.
            url (str, optional): The URL to include in the post.

        Returns:
            dict or None: A dictionary containing the JSON response from the Facebook API, or None if an error occurred.

        Raises:
            Exception: If there is an error creating the post, the error message is printed.
        """
        data = {
            "access_token": self.PAGE_ACCESS_TOKEN,
            "message": text,
            "link": url
        }
        try:
            response = requests.post(self.PAGE_FEED_ENDPOINT, data=data)
        except Exception as e:
            print(f"Error creating Facebook text post: {e}")
            return None
        return response.json()
