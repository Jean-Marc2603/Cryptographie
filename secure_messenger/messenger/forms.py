from django import forms
from django.contrib.auth.models import User
from .models import Message

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Destinataire"
    )
    content = forms.CharField(
        widget=forms.Textarea,
        label="Message"
    )

    class Meta:
        model = Message
        fields = ['recipient', 'content']