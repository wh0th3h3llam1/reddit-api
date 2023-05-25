from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True

    @property
    def added_on(self):
        return self.created

    @property
    def updated_on(self):
        return self.modified

    def save(self, *args, **kwargs):
        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except Exception as e:  # Catch field does not exist exception
                    pass
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)
