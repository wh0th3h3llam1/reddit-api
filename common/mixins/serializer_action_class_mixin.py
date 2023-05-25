from typing import Any, Dict


class SerializerActionClassMixin:
    """
    A class which inhertis this mixin should have attribute
    `serializer_action_classes`.

    Look for serializer class in self.serializer_action_classes, which
    should be a dict mapping action name (key) to serializer class (value),
    i.e.:

    ```
    class SampleViewSet(viewsets.ModelViewSet):
        serializer_class = DocumentSerializer
        serializer_action_classes = {
            'upload': UploadDocumentSerializer,
            'download': DownloadDocumentSerializer,
        }

        @action(method=["get"], detail=False)
        def upload():
            ...
    ```

    If there's no entry for that action then just fallback to the regular
    get_serializer_class.
    `lookup`: self.serializer_class, DefaultSerializer.
    """

    serializer_action_classes: Dict[str, Any]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "serializer_action_classes"):
            raise AttributeError(
                "class '%s' must include `serializer_action_classes` attribute"
                % cls.__name__
            )

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
