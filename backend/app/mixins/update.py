from django.db import models


class UpdateFieldsMixin(models.Model):
    class Meta:
        abstract = True

    def update_fields(self, update_data):
        for field, data in update_data.items():
            if data is not None:
                setattr(self, field, data)
