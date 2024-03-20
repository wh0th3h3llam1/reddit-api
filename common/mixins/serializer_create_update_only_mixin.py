from rest_framework import serializers


class SerializerCreateUpdateOnlyMixin(serializers.ModelSerializer):
    """
    Mixin which allows fields to populate for creating only or updating only
    It looks for the `create_only_fields` or `update_only_fields` attribute of
    `Meta` class of the serializer


    ```
    class MySerializer(CreateOnlyMixin, serializers.ModelSerializer):
        ...

        class Meta:
            ...
            create_only_fields = ("name", "owner")
            update_only_fields = ("archived",)
    ```
    """

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        create_only_fields = getattr(self.Meta, "create_only_fields", None)
        update_only_fields = getattr(self.Meta, "update_only_fields", None)

        if self.instance and create_only_fields:
            if not isinstance(create_only_fields, (list, tuple)):
                raise TypeError(
                    "The `create_only_fields` option must be a list or tuple. "
                    "Got %s." % type(create_only_fields).__name__
                )

            model_fields = self.Meta.model._get_field_names()

            for field in create_only_fields:
                assert field in model_fields, (
                    "The field '{field_name}' was included on serializer "
                    "{serializer_class} in the `create_only_fields` option, but does "
                    "not match any model field.".format(
                        field_name=field,
                        serializer_class=self.__class__.__name__,
                    )
                )
                kwargs.setdefault(field, {})
                kwargs[field]["read_only"] = True

        # if self.instance is None and update_only_fields:
        #     if not isinstance(update_only_fields, (list, tuple)):
        #         raise TypeError(
        #             "The `update_only_fields` option must be a list or tuple. "
        #             "Got %s." % type(update_only_fields).__name__
        #         )

        #     for field in update_only_fields:
        #         self.initial_data.pop(field, None)
        #         kwargs.setdefault(field, {})
        #         kwargs.pop(field, None)

        return kwargs
