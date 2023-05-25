class PermissionActionClassMixin(object):

    """
    A class which inhertis this mixins should have variable
    `permission_action_classes`.

    Look for permission class in self.serializer_action_classes, which
    should be a dict mapping action name (key) to permission class (value),
    i.e.:

    ```
    class SampleViewSet(viewsets.ModelViewSet):
        permission_classes = (IsAuthenticated,)
        permission_action_classes = {
            "create": (IsAuthenticated,),
            "list": (IsAuthenticated,),
            "update": (IsAdminOrSuperAdmin,),
            "partial_update": (IsAdminOrSuperAdmin,),
            "destroy": (IsSuperAdmin,)
        }
    ```

    If there's no entry for that action then just fallback to the regular
    get_permissions.
    `lookup`: self.permission_classes
    """

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission()
                for permission in self.permission_action_classes[self.action]
            ]
        except (AttributeError, KeyError):
            # action is not set return default permission_classes
            return super().get_permissions()
