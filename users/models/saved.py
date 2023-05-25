# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.db import models

# from core.models import BaseModel
# from .user import User


# class Saved(BaseModel):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="saved")

#     # the required fields to enable a generic relation
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()


# # https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html


# #! Delete is not possible in GenericRelations


# # # Add a new instance of Comment
# # comment = Comment.objects.create(text='This is a test comment')

# # # Like the comment
# # Saved.objects.create(user=request.user, content_object=comment)
