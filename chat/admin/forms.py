from django import forms

from chat.models import Message


class MessageAdminForm(forms.ModelForm):
    def clean(self):
        replied = self.cleaned_data.get("replied_to", None)
        room = self.cleaned_data.get("room")

        if replied is not None:
            if self.instance is not None:
                if replied.id != self.instance.id:
                    self.add_error(
                        "replied_to", "No such message can be replied to"
                    )

            if not Message.objects.filter(id=replied.id, room=room.id).exists():
                self.add_error(
                    "replied_to", "No such message can be replied to"
                )

        return self.cleaned_data
