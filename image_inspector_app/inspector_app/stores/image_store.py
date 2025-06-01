from inspector_app.models import ImageClassificationLedger


class ImageStore:

    def create_bulk_image_classification_ledger(self, data):
        ImageClassificationLedger.objects.bulk_create(data)
