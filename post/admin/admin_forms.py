from django import forms

from post.models import Comment, Post
from post.utils import make_post_slug


class PostAdminForm(forms.ModelForm):
    def clean(self):
        if self.instance is None:
            title = self.cleaned_data["title"]
            slug = make_post_slug(title)
            self.cleaned_data["slug"] = slug

        return self.cleaned_data

    class Meta:
        model = Post
        fields = "__all__"


class CommentAdminForm(forms.ModelForm):
    def clean(self):
        parent = self.cleaned_data.get("parent", None)
        post = self.cleaned_data.get("post")

        if parent is not None:
            if parent.id == self.instance.id:
                self.add_error(
                    field="parent",
                    error="Parent comment cannot be same as current",
                )
            if not Comment.objects.filter(id=parent.id, post=post).exists():
                self.add_error(
                    field=None,
                    error="Parent comment doesn't belong to the Post",
                )

        return self.cleaned_data

    class Meta:
        model = Comment
        fields = "__all__"
