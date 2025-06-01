from celery import shared_task
from inspector_app.models import ImageClassificationLedger
from inspector_app.stores.image_store import ImageStore

import base64
from PIL import Image
from io import BytesIO
from cloudinary.uploader import upload
from image_inspector_app.utils.cloudinary_config import configure_cloudinary
from image_inspector_app.utils.time_manager import TimeManager


@shared_task
def create_image_classification_ledger(order_id, image, classification_data):

    """
    Save image and create ledger entry
    """

    time_manager = TimeManager()
    configure_cloudinary()
    classification_data_list = []

    # Decode base64 image
    image_data = base64.b64decode(image)
    image = Image.open(BytesIO(image_data))

    # Convert to file-like object
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    # Upload to Cloudinary
    response = upload(buffer, folder="orders", public_id="order_" + str(order_id), overwrite=True)

    # Get the image key (public_id or URL)
    # https://res.cloudinary.com/{cloud_name}/image/upload/{public_id}.{format}
    image_key = response.get("public_id")

    for data in classification_data:
        classification_data_list.append(
            ImageClassificationLedger(
                order_id=data.get("order_id"),
                top_label=data.get("top_label"),
                confidence=data.get("confidence"),
                is_valid=data.get("is_valid_image"),
                image_key=image_key,
                n_slot_id=time_manager.get_yymmdd(),
                created_epoch=time_manager.get_current_epoch()
            )
        )

    # Create ledger entry in bulk
    if classification_data_list:
        ImageStore().create_bulk_image_classification_ledger(classification_data_list)
