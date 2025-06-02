from rest_framework.exceptions import APIException
from inspector_app.validators import PayLoadValidator, ImageValidator
from inspector_app.constants import LABELS, THRESHOLD, TOP_PREDICTION_COUNT

from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

from inspector_app.tasks import create_image_classification_ledger
from io import BytesIO
import base64


class OrderImageManager:

    def __init__(self):
        self.payload_validator = PayLoadValidator()
        self.image_validator = ImageValidator()
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def inspect_and_validate_image(self, order_id, image_file):

        img_classification_data = []

        # Validate payload
        self.payload_validator.validate_order_and_image(order_id, image_file)

        # Validate image dimensions
        image_file = image_file[0]  # Access the image
        image = Image.open(image_file).convert("RGB")  # convert to RGB colors
        self.image_validator.validate_image_dimensions(image)

        # Labels
        valid_labels = set(LABELS)

        try:

            # Prepare input for the model
            inputs = self.processor(text=LABELS, images=image, return_tensors="pt", padding=True)

            # Feed inputs to the model
            outputs = self.model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)[0]

            # Get Top-K predictions labels
            top_k = torch.topk(probs, k=TOP_PREDICTION_COUNT)
            top_indices = top_k.indices.tolist()
            top_confidences = top_k.values.tolist()

            # Check if any top-K label is valid and above threshold
            threshold = THRESHOLD
            for idx, conf in zip(top_indices, top_confidences):
                label = LABELS[idx]
                if label in valid_labels and conf > threshold:
                    img_classification_data.append({
                        "order_id": order_id,
                        "top_label": label,
                        "confidence": round(conf, 3),
                        "is_valid_image": True
                    })

                    # Save image to memory and convert image to base64 format
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    image_base64 = base64.b64encode(buffered.getvalue()).decode()

                    # Create classification ledger for the image
                    create_image_classification_ledger.delay(order_id, image_base64, img_classification_data)
                    return {
                        "order_id": order_id,
                        "top_label": label,
                        "confidence": round(conf, 3),
                        "contains_valid_item": True
                    }

            # If none of the top K matched
            img_classification_data.append({
                "order_id": order_id,
                "top_label": LABELS[top_indices[0]],
                "confidence": round(top_confidences[0], 3),
                "is_valid_image": False
            })

            # Create classification ledger for the image
            # Save image to memory and convert image to base64 format
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            create_image_classification_ledger.delay(order_id, image_base64, img_classification_data)

            return {
                "order_id": order_id,
                "top_label": LABELS[top_indices[0]],
                "confidence": round(top_confidences[0], 3),
                "contains_valid_item": False
            }

        except Exception as e:
            print(e)
            raise APIException("Something went wrong.")
