from inspector_app.exceptions.default_exception import DefaultException
from inspector_app.constants import MIN_IMAGE_WIDTH, MAX_IMAGE_HEIGHT


class PayLoadValidator:

    def validate_order_and_image(self, order_id, image_file):
        """
        Validate payload -
        1. order_id and image file are required
        2. allow processing of one image only
        """
        if not order_id:
            raise DefaultException("No order id provided.")

        if not image_file:
            raise DefaultException("No image file provided.")

        if len(image_file) > 1:
            raise DefaultException("Cannot process more than one photo.")


class ImageValidator:

    def validate_image_dimensions(self, image):
        """
        Validate image dimensions
        """
        image_width = image.size[0]
        image_height = image.size[1]
        if image_width < MIN_IMAGE_WIDTH or image_height < MAX_IMAGE_HEIGHT:
            raise DefaultException("Image resolution too small: {}x{}".format(image_width, image_height))
