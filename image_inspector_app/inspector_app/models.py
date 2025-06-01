from django.db import models


class ImageClassificationLedger(models.Model):
    """
    Model to store image classification data
    """
    order_id = models.IntegerField(db_index=True)
    top_label = models.CharField(max_length=50, default="")
    confidence = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    is_valid = models.BooleanField(default=False)
    image_key = models.CharField(max_length=50, default="")
    n_slot_id = models.IntegerField(db_index=True, default=0)
    created_epoch = models.IntegerField(db_index=True, default=0)

    class Meta:
        managed = True
        db_table = "image_classification_ledger"
