from PIL import Image
from io import BytesIO
import os


class FileService:
    @staticmethod
    def update_image(user, data):
        image = data['image']
        # Crop logic using `top`, `left`, `height`, and `width` can be added
        # For example, crop using PIL
        # Save the updated image
        user.profile_image.save(image.name, image)
        return user


class FileService:
    @staticmethod
    def add_video(post, video):
        """
        Handles video upload for a post.
        """
        post.video.save(video.name, video)
        return post
