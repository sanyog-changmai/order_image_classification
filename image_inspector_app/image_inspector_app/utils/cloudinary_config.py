import cloudinary
from image_inspector_app.settings import CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_SECRET_KEY


def configure_cloudinary():
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_SECRET_KEY
    )
