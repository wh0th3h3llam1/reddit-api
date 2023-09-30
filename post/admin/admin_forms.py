from django import forms

from post.models import Comment


class CommentAdminForm(forms.ModelForm):
    def clean(self):
        parent = self.cleaned_data.get("parent", None)
        post = self.cleaned_data.get("post")

        if parent is not None:
            if not Comment.objects.filter(id=parent.id, post=post).exists():
                raise forms.ValidationError(
                    "Parent Comment doesn't belong to the Post"
                )

        return self.cleaned_data

    class Meta:
        model = Comment
        fields = "__all__"
